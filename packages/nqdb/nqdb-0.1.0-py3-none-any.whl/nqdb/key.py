# Luca de Alfaro, 2020
# BSD License

import json
from numbers import Integral


class Key(object):
    """This class mimics a datastore Key, with the difference that it is initialized
    using a nqdb.Model instance rather than just a string.  It has only one method, get,
    which returns the given entity."""

    def __init__(self, model_class, *args):
        """
        A key is build from:
        :param model_class: Model class.
        :param args: ids of the key.
        Example: Key(MyEntity, 34)
        """
        for a in args:
            assert isinstance(a, str) or isinstance(a, Integral)
        self.model_class = model_class
        self.ids = args

    @property
    def kind(self):
        return self.model_class._model_kind()

    def __repr__(self):
        return ("%s(%s)" % (self.kind,
            " ,".join([repr(id) for id in self.ids])))

    def get(self):
        """Creates a model."""
        m = self.model_class(*self.ids)
        return m.get()

    def delete(self):
        m = self.model_class(*self.ids)
        return m.delete()

    @property
    def path(self):
        """Returns a path that can be used for caching purposes."""
        return json.dumps([self.kind] + list(self.ids))
