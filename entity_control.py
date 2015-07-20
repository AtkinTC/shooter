from entity import *

entity_dict = None
large = None
kill_set = set()

def init():
    global entity_dict, large
    entity_dict = {}
    large = -1

def register(entity):
    global entity_dict, large
    id = 0
    while id in entity_dict:
        id += 1
    large = max(large, id)
    entity_dict[id] = entity
    entity.set_id(id)
    return id

def yield_entities():
    for k in entity_dict.copy():
        yield entity_dict[k]

def kill_entity(id):
    global kill_set
    kill_set.add(id)

def kill_finalize():
    global kill_set, entity_dict
    for k in kill_set:
        entity_dict.pop(k)
    kill_set = set()
