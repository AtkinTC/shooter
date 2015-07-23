from entity import *

entity_dict = {}
kill_set = set()

def init():
    global entity_dict
    entity_dict = {}

def register(entity, id = None):
    global entity_dict
    if not id:
        id = 0
        while id in entity_dict:
            id += 1
    entity_dict[id] = entity
    entity.set_id(id)
    return id

def yield_entities():
    for k in entity_dict.copy():
        yield entity_dict[k]

def get_entity(id):
    return entity_dict.get(id, None)

def kill_entity(id):
    global kill_set
    kill_set.add(id)

def kill_finalize():
    global kill_set, entity_dict
    for k in kill_set:
        entity_dict.pop(k)
    kill_set = set()
