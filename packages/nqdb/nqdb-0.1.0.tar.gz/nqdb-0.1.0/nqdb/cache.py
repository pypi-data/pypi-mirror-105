# Luca de Alfaro, 2020
# BSD License

class Cache(object):
    """Mock cache used for testing.  Real cache implementations
    must have the same signature. """

    def __init__(self):
        self.c = {}

    def get(self, k):
        return self.c.get(k)

    def get_multi(self, klist):
        return [self.get(k) for k in klist]

    def set(self, k, v, expiry=None):
        """expiry is the expiration deadline in seconds."""
        self.c[k] = v

    def set_multi(self, d, expiry=None):
        """Performs all updates specified by a dictionary d."""
        self.c.update(d)

    def delete(self, k):
        del self.c[k]

    def delete_multi(self, klist):
        for k in klist:
            self.delete(k)

    def clear(self):
        self.c = {}

    def __repr__(self):
        return repr(self.c)


