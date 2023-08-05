# Luca de Alfaro, 2020
# BSD License


class Query(object):
    """Implements a query, wrapping each result in our model."""

    def __init__(self, cls, kind, order=()):
        """Creates a query for a given model class.
        :param cls: class for which the query applies.
        :param kind: kind for the query.
        """
        self.cls = cls
        self.kind = kind
        self.q = cls._client.client.query(kind=kind, order=order)

    def filter(self, f):
        """Adds a filter to the query.
        :param f: filter added.  A filter is a tuple,
        consisting of property, operator, value.
        """
        self.q.add_filter(*f)

    def order(self, *fields):
        """Adds an ordering to a query."""
        self.q._order = tuple(fields)

    def fetch(self, keys_only=False, **kwargs):
        """Returns an iterator.  This is the datastore interface, with more options."""
        if keys_only:
            self.q.keys_only()
            for k in self.q.fetch(**kwargs):
                yield k
        else:
            for e in self.q.fetch(**kwargs):
                yield self.cls.wrap_entity(e)

    def get(self):
        """Returns the first result only, or None if there is none."""
        for e in self.q.fetch():
            return e
        return None

    # NDB interface
    iter = fetch
