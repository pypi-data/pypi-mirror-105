# Luca de Alfaro, 2020
# BSD License


def get_multi(keys, use_cache=True):
    """Gets many keys in parallel.
    :param keys: list of nqdb.Key to get.
    :param use_cache: set to False if you wish to avoid using the cache even
        when available.
    """
    if len(keys) == 0:
        return []
    # First, fishes out the client and entity name from the first model.
    k0 = keys[0]
    _client = k0.model_class._client
    model_class = k0.model_class
    # Checks that the model class and clients are the same.
    # The model class being the same is a limitation due to the idiotic API
    # google provides; otherwise it's hard to associate the found data
    # back to the original types.
    for k in keys[1:]:
        assert _client == k.model_class._client
        assert k.model_class == model_class
    # First, tries to use the cache to get as many as possible.
    if _client.cache is not None and use_cache:
        cache_string_r = _client.cache.get_multi([k.path for k in keys])
    else:
        cache_string_r = [None] * len(keys)
    # Builds the list of entities found in the cache.
    results_from_cache = [model_class.from_string(s) for s in cache_string_r if s is not None]
    # Does a get_multi to get the other results.
    missing_keys = [k for i, k in enumerate(keys) if cache_string_r[i] is None]
    # Builds the list of keys according to the client.
    missing_client_keys = [_client.client.key(model_class._model_kind(), *k.ids) for k in missing_keys]
    # Gets the entities, wrapping the result in our Model class.
    # Ok.  I have to write it.  get_multi has one of the most inane APIs that
    # I have ever seen.  It's just completely idiotic that the missing entries are
    # not just reported as None, as part of the list.
    found_entities = _client.client.get_multi(missing_client_keys)
    wrapped_found_entities = [model_class.wrap_entity(e) for e in found_entities]
    results = results_from_cache + wrapped_found_entities
    # Read hook.
    for e in results:
        for prop in e._properties.values():
            prop.read_hook(e)
    return results


def get(key, **kwargs):
    """
    Gets a NQDB Key, returning the entity.
    :param key: key to get.
    """
    r = get_multi([key], **kwargs)
    return None if len(r) == 0 else r[0]


def delete_multi(keys):
    """Deletes a list of keys.
    :param keys: list of NQDB Keys to be deleted."""
    if len(keys) == 0:
        return []
    # First, fishes out the client from the first model.
    k0 = keys[0]
    _client = k0.model_class._client
    # Checks that the client is the same, otherwise we are in trouble.
    for k in keys[1:]:
        assert _client == k.model_class._client
    # Deletes from the cache.
    if _client.cache is not None:
        _client.cache.delete_multi([k.path for k in keys])
    # Builds the list of keys according to the client.
    client_keys = [_client.client.key(k.kind, *k.ids) for k in keys]
    _client.client.delete_multi(client_keys)


def delete(key):
    """Deletes one key.
    :param key: NQDB Key to delete"""
    delete_multi([key])


def put_multi(entities, use_cache=True, expiry=None):
    """Puts multiple entities in parallel.  The entities should be
    objects of NQDB models of course.
    :param entities: List of NQDB entities to write.
    :param use_cache: if False, then an entry, if existing, is deleted
        from the cache.  Use this to avoid filling the cache.
    :param expiry: expiry time for the cache.
    """
    if len(entities) == 0:
        return
    for e in entities:
        e._complete_entity()
        # Write hook for defaults.
        for prop in e._properties.values():
            prop.write_hook(e)
    # Gets the client, and checks that the client is the same for all.
    _client = entities[0].__class__._client
    for e in entities[1:]:
        assert e.__class__._client == _client
    # Gets the client.
    client_entities = [e._entity for e in entities]
    _client.client.put_multi(client_entities)
    # Puts in the cache, if any.  Note that we have to do this AFTER
    # we write to the store, as the real key may not be known until then.
    if _client.cache is not None:
        if use_cache:
            _client.cache.set_multi({e.key.path: e.to_string() for e in entities},
                                    expiry=expiry)
        else:
            # We need to delete from the cache, in case some (now old)
            # values were cached.
            _client.cache.delete_multi([e.key.path for e in entities])


def put(entity, use_cache=True, expiry=None):
    """Writes a single entity.
    :param entity: entity to be written.
    :param use_cache: if False, then the entity, if existing, is deleted
        from the cache.  Use this to avoid filling the cache.
    :param expiry: expiry time for the cache."""
    put_multi([entity])
