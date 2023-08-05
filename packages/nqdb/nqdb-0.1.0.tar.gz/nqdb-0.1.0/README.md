# NQDB

Not quite the DB Google used to have, not quite the DB Google has now. 
Of course, better than both.

This is a mock of NDB, almost. 
It enables interfacing to Google Datastore, or to other DBs, by 
changing the client. 

## Usage

### Models
```python
from nqdb import *

client = DatastoreClient()

class Person(Model):
    _client = client
    first_name = StringProperty('first_name')
    last_name = StringProperty('last_name')

p = Person()
p.first_name = "Luca"
p.last_name = "de Alfaro"
p.put()
id = p.key_id
print("id:", id)
q = Person(id=id)
q.get()
print("First name:", q.first_name)
print("Last name:", q.last_name)
```

### Keys

```python
p = Person()
p.first_name = "Joe"
p.last_name = "Falchetto"
put(p)
id = p.key_id
k = Key(Person, id)
q = k.get()
```
    
### Batch operations

```python
from nqdb import put_multi

p = Person()
p.first_name = "Joe"
p.last_name = "Falchetto"
q = Person()
q.first_name = "Luca"
q.last_name = "de Alfaro"
put_multi([p, q])
```

The client used by `put_multi` is derived from the client used for `p` and `q`. 
You cannot mix in the same batch operations models with different clients.

### Queries

```python
q = Person.query()
q.filter(Person.first_name == 'Luca')
q.filter(Person.gender == 'Male')
for p in q.fetch():
    print(p.last_name)
```
        
You can add an ordering to a query by: 
    
```python
q.order(+Person.first_name)
```
    
You can use both `+Person.first_name` and `-Person.first_name`, 
but one of `+`, `-` should be present. 
        
### Caching

```python
client = DatastoreClient(cache=MyCache())
```

Look at `cache.Cache` to see the (very few) methods you need to implement to use a new cache. 


And as usual, look at the test files, because those do not lie. 
