# Luca de Alfaro, 2020
# BSD License


from .client import NQDBClient
from .datastore_mock import Client as MockClient, Entity as MockEntity, Key as MockKey
from google.cloud.datastore import Client, Entity, Key


class DatastoreClient(NQDBClient):

    def __init__(self, cache=None, mock=False):
        """Creates a datastore client.
        :param cache: optional object implementing the cache, with the
        signature of cache.Cache.
        :param mock: if true, builds a mock client.
        """
        super().__init__()
        self.cache = cache
        if mock:
            self.client = MockClient()
            self.Entity = MockEntity
            self.Key = MockKey
        else:
            self.client = Client()
            self.Entity = Entity
            self.Key = Key




