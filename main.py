import pickle
from os import path, remove
from datetime import datetime
from uuid import uuid4

class Item:
    def __init__(self, obj, id: str = None, name: str = None):
        self.obj = obj
        self.created = self.changed = datetime.now()
        self.id = id if id else str(uuid4())
        self.hash = hash(self)

        if name:
            self.name = name

    def check_change(self):
        if hash(self) != self.hash:
            self.changed = datetime.now()

    @property
    def type(self):
        return type(self.obj)

    @property
    def raw(self):
        return self.obj

    @property
    def describe(self):
        print(
            f'''
            Type: {self.type}
            Name: {self.obj.__class__.__name__}
            ID: {self.id}
            Date Created: {self.created}
            Date changed: {self.changed}            
            data: {self.obj}            
            '''
        )

class Filter:
    objects = ...

    def __init__(self, manage: object, key: str, value: str):
        self.manage = manage
        self.key = key
        self.value = value
        self.objects = []

        self.do()

    def do(self):
        self.objects = list(filter(lambda x: x[self.key] == self.value, [item for item in self.manage.objects_list() if isinstance(item, dict)]))

    def first(self) -> objects or None:
        if len(self.objects) > 0:
            return self.objects[0]
        return None

    def last(self) -> objects or None:
        if len(self.objects) > 0:
            return self.objects[0]
        return None

    def all(self):
        return self.objects
class DataToLocal:
    db_name = 'DataToLocal.pkl'
    path_location = '.'
    logs = False
    _cache: dict = None

    def __init__(self):
        self.load()

    @property
    def full_path(self):
        return path.join(self.path_location, self.db_name)

    def items(self):
        return self._cache['items']

    def keys(self):
        return self.items().keys

    def values(self):
        return self.items().values()

    def objects_list(self):
        return [value.raw for value in self._cache['items'].values()]

    def console(self, message):
        if self.logs:
            print(message)

    def load(self):
        # Create new file
        if not path.exists(self.full_path):
            _init_template = {
                'items': {},
                'created': datetime.now(),
            }

            _init_template['changed'] = _init_template['created']

            self._cache = _init_template

        self.commit()

        # Read existed file
        with open(self.full_path, 'rb') as file:
            self._cache = pickle.load(file)
            return self._cache

    def commit(self):
        if not self._cache:
            self.console("Local file are not exist!")
        else:
            with open(self.full_path, 'wb') as file:
                pickle.dump(self._cache, file, pickle.HIGHEST_PROTOCOL)
                self.console("DB has been saved!")
        return self

    def append(self, obj: object, name: str = None, id: object = None) -> Item:
        self._cache = self.load()

        item = Item(obj=obj, id=id, name=name)

        self._cache['items'][item.id] = item
        self.commit()

        return self.get_by_id(item.id)

    def get_by_id(self, id):
        return self._cache['items'][id]

    def get(self, item: object) -> object:
        return self._cache['items'][item.id].raw

    def delete(self, item: object):
        del self.load()['items'][item.id]
        self.commit()

    def reset(self, force=False):
        def remove_file():
            if path.exists(str(self.full_path)):
                remove(str(self.full_path))
                return self.load()

        if force:
            remove_file()
        else:
            selection = input("Reset the data: y/n")
            if selection.lower() == 'y':
                remove_file()
            else:
                self.console("Reset operation canceled!")

    def filter(self, key, value):
        return Filter(self, key, value)
    def get_by_name(self, name: str, ignore= False) -> object or None:
        keyword = name.lower() if ignore else name

        for item in self.values():
            if hasattr(item, 'name'):
                item_name = item.lower() if ignore else item.name
                if item_name == keyword:
                    return item.raw
        return None

x = DataToLocal()
x.append({'age': 13, 'name': 'dvir'}, name='dvir')
a = x.get_by_name('dvir')
x.commit()

print(a)









