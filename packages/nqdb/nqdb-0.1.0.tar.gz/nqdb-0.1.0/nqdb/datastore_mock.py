# Luca de Alfaro, 2020
# BSD License

"""
Mock for testing of datastore classes.
"""

import uuid
import contextlib

DATASTORE = {}


class Entity(dict):
    def __init__(self, key=None, exclude_from_indexes=()):
        super().__init__()
        assert key is None or isinstance(key, Key)
        assert isinstance(exclude_from_indexes, tuple)
        self.key = key
        self.exclude_from_indexes = exclude_from_indexes

    def put(self):
        self.key.put(self)


class Key(object):
    def __init__(self, kind, *a):
        self.kind = kind
        self.path = a

    @property
    def id_or_name(self):
        return "/".join(str(x) for x in self.path)

    @property
    def _full_path(self):
        return self.kind + "/" + self.id_or_name

    def get(self):
        return DATASTORE.get(self._full_path)

    def put(self, v):
        if len(self.path) == 0 or self.path[0] is None:
            # There is no key. We create one at random.
            self.path = [str(uuid.uuid4())]
        DATASTORE[self._full_path] = v

    def delete(self):
        if self._full_path in DATASTORE:
            del DATASTORE[self._full_path]


class Client(object):

    def key(self, kind, *a):
        return Key(kind, *a)

    def get(self, key):
        """Reads an Entity."""
        return key.get()

    def get_multi(self, klist):
        """I know it is idiotic, but the datastore function just returns the
        existing entities without clear indication of which entities are missing."""
        return [e for e in [k.get() for k in klist] if e is not None]

    def put(self, e):
        """Writes an entity"""
        e.put()

    def put_multi(self, elist):
        for e in elist:
            e.put()

    def delete(self, key):
        return key.delete()

    def delete_multi(self, klist):
        return [k.delete() for k in klist]

    def transaction(self):
        return contextlib.AbstractContextManager()

