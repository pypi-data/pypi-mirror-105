# Luca de Alfaro, 2020
# BSD License

import functools

class NQDBClient(object):
    """Abstract client implementation for NQDB"""
    def __init__(self):
        self.client = None
        self.Entity = None
        self.Key = None
        self.cache = None

    def transactional(self, fn):
        """Performs fn inside a transaction.  Unfortunately this needs to be
        a client method, because a transaction may involve multiple models."""
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            with self.client.transaction():
                return fn(*args, **kwargs)
        return wrapped
