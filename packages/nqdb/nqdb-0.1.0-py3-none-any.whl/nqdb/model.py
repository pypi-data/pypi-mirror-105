# Luca de Alfaro, 2020
# BSD License

import json
from numbers import Integral

from .property import Property
from .client import NQDBClient
from .query import Query
from .nqdb_ops import get as nqdb_get, put as nqdb_put, delete as nqdb_delete
from .key import Key

"""
Example of use:

class Person(Model):

    _client = DatastoreClient(cache=None)
    _kind = "Person" # Optional; useful only if different from class name.

    first_name = StringProperty('first_name')
    last_name = StringProperty('last_name')
    

p = Person()
p.first_name = "Luca"
p.last_name = "de Alfaro"
p.put()
id = p.key_id

q = Person(id="my-data-id")
q.read()
print(q.first_name)

# or

k = Key(Person, id)
q = k.get()
"""


class Model(object):
    """A datastore model."""

    # You should override this class-level client.
    _client = NQDBClient()

    # You should also over-ride this if desired.
    # Otherwise, it will default to class name.
    _kind = None

    def __init__(self, id=None, key=None, _entity=None, **kwargs):
        """
        Declares a model.
        :param id: string or integer id of an entity, or a list of such.
        :param key: datastore key for an entity.
        :param _entity: A Datastore entity, can be used to initialize the model.
        :param kwargs: Additional keyword arguments that are used, after
            initialiation, to initialize properties of the model.
        """
        assert (
            id is None
            or isinstance(id, str)
            or isinstance(id, Integral)
            or isinstance(id, list)
        )
        if isinstance(id, list):
            for el in id:
                assert isinstance(el, str) or isinstance(el, Integral)
        assert key is None or isinstance(key, self.nqdb_client.Key)
        assert id is None or key is None
        # Gets the kind.
        # We produce a key for the entity.
        if key is not None:
            assert key.kind == self._model_kind()
            k = key
        elif isinstance(id, list):
            k = self.nqdb_client.client.key(*([self._model_kind()] + id))
        elif id is not None:
            k = self.nqdb_client.client.key(self._model_kind(), id)
        else:
            # This is an incomplete key, that will be completed at writing.
            k = self.nqdb_client.client.key(self._model_kind())
        # Dictionary mapping names to properties.
        self._properties = {}
        # List of non-indexed property names.
        self._no_index = []
        for prop_name, prop in self.__class__.__dict__.items():
            if isinstance(prop, Property):
                self._properties[prop_name] = prop
                if not prop._indexed:
                    self._no_index.append(prop_name)
        # This is the Entity that keeps the mapping for the database.
        if _entity is None:
            # Creating an entity.
            self._entity = self.nqdb_client.Entity(key=k, exclude_from_indexes=tuple(self._no_index))
            # Initialization hook for properties.
            for prop in self._properties.values():
                prop.init_hook(self)
        else:
            # The entity has been read.
            # If we specified a key, we set it.
            if key is not None:
                _entity.key = key
            self._entity = _entity
            self._entity.exclude_from_indexes = self._no_index
        # Takes care of other initialization parameters.
        for prop_name, prop_value in kwargs.items():
            self._properties[prop_name].__set__(self, prop_value)

    @classmethod
    def _model_kind(cls):
        return cls._kind or cls.__name__

    @property
    def key_id(self):
        return self._entity.key.id_or_name

    @property
    def key(self):
        """Returns the nqdb key for the entity
        (NOT the client key, which is in self._entity.key)"""
        return Key(self.__class__, self.key_id)

    @property
    def nqdb_client(self):
        return self.__class__._client

    def _complete_entity(self):
        """Utility method that ensures the entity has a key."""
        if self._entity.key is None:
            self._entity.key = self.nqdb_client.client.key(self._model_kind())

    def get(self, **kwargs):
        """Reads the entity, assuming the key is not empty."""
        assert self._entity.key.id_or_name is not None
        e = nqdb_get(self.key, **kwargs)
        self._entity = e._entity
        # Read hook for defaults.
        for prop in self._properties.values():
            prop.read_hook(self._entity)
        return self

    def put(self, use_cache=True, expiry=None):
        """Writes itself to datastore.
        :param use_cache: if False, then an entry, if existing, is deleted
        from the cache.  Use this to avoid filling the cache.
        :param expiry: expiry time for the cache.
        """
        # If there is no key, we need to produce a key that contains the
        # entity kind at least.
        nqdb_put(self, use_cache=use_cache, expiry=expiry)

    def delete(self):
        """Deletes itself from the datastore."""
        assert self._entity.key.id_or_name is not None
        nqdb_delete(self._entity.key)

    # Support for serialization.
    def to_string(self):
        d = {
            "kind": self._model_kind(),
            "key_id": self.key_id,
            "props": {n: v.to_json(self) for n, v in self._properties.items()}
        }
        return json.dumps(d)

    @classmethod
    def from_string(cls, s):
        d = json.loads(s)
        assert d["kind"] == cls._model_kind()
        e = cls(id=d["key_id"])
        for n, v in e._properties.items():
            v.from_json(e, d["props"][n])
        return e

    # Nicknames
    write = put
    read = get

    @classmethod
    def wrap_entity(cls, entity):
        """Wraps an entity, which might have been read in a different way,
        as an entity of this type."""
        assert entity.key.kind == cls._model_kind()
        return cls(key=entity.key, _entity=entity)

    @classmethod
    def query(cls, *args):
        """
        Builds a query. Usage:

        q = Person.query()
        q.filter(Person.age > 10)
        or:
        q = Person.query(Person.age > 10, Person.height < 100)
        for p in q.fetch():
            ...
        :param *args: Arguments added to the query.
        """
        q = Query(cls, cls._model_kind())
        for a in args:
            q.filter(*a)
        return q


Property.__reserved__ = {"key", "key_id", "read", "get", "write", "put", "wrap"}
for f in dir(Model):
    if not f.startswith("_"):
        Property.__reserved__.add(f)
for f in dir(Property):
    if not f.startswith("_"):
        Property.__reserved__.add(f)

