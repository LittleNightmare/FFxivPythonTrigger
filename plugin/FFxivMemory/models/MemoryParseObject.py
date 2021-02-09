from plugin.FFxivMemory.MemoryHandler import MemoryHandler
from time import time
auto_update_sec = 0.5

class Base(object):
    vals = dict()

    def __init__(self, handler: MemoryHandler, base: int):
        self.handler = handler
        self.base = base
        self.cache = dict()
        self.last_update = dict()

    def need_update(self,key):
        return self.last_update[key]+auto_update_sec>time()

    def __getattr__(self, key):
        return self[key]

    def __getitem__(self, key):
        if key not in self.vals:
            raise IndexError('%s is not a valid key' % key)
        return self.refresh(key) if self.need_update(key) else self.cache[key]

    def refresh(self, key):
        if type(self.vals[key][0]) == str:
            if self.vals[key][0] == 'bytes':
                self.cache[key] = self.handler.read_bytes(self.base + self.vals[key][2], self.vals[key][1])
            else:
                self.cache[key] = getattr(self.handler, 'read_' + self.vals[key][0])(self.base + self.vals[key][1])
        else:
            self.cache[key] = self.vals[key][0](self.handler, self.base + self.vals[key][1])
        self.last_update[key] = time()
        return self.cache[key]

    def __setitem__(self, key, value):
        if key not in self.vals:
            raise IndexError('%s is not a valid key' % key)
        if type(self.vals[key][0]) == str:
            if self.vals[key][0] == 'bytes':
                self.handler.write_bytes(self.base + self.vals[key][2], value, self.vals[key][1])
            else:
                getattr(self.handler, 'write_' + self.vals[key][0])(self.base + self.vals[key][1], value)
        else:
            self.cache[key].replace(value)
        self.refresh(key)

    def replace(self, value):
        for key in self.vals:
            self[key] = value[key]


class MemoryObject(Base):
    def __init__(self, handler: MemoryHandler, base: int):
        super(MemoryObject, self).__init__(handler, base)
        for key in self.vals:
            self.refresh(key)


class MemoryLazyObject(Base):
    def __getitem__(self, key):
        if key not in self.vals:
            raise IndexError('%s is not a valid key' % key)
        return self.refresh(key) if key not in self.cache or self.need_update(key) else self.cache[key]


def get_memory_class(vals_data: dict):
    class TempClass(MemoryObject):
        vals = vals_data

    return TempClass


def get_memory_lazy_class(vals_data: dict):
    class TempClass(MemoryLazyObject):
        vals = vals_data

    return TempClass


class MemoryArray(object):
    Length = 0
    ValType = None
    ValLen = 0

    def __init__(self, handler: MemoryHandler, base: int):
        self.handler = handler
        self.base = base
        self.cache = [None for i in range(self.Length)]
        for i in range(self.Length): self.refresh(i)

    def refresh(self, key: int):
        if type(self.ValType) == str:
            self.cache[key] = getattr(self.handler, 'read_' + self.ValType)(self.base + (self.ValLen * key))
        else:
            self.cache[key] = self.ValType(self.handler, self.base + (self.ValLen * key))
        return self.cache[key]

    def __getitem__(self, key):
        return self.cache[key]

    def __setitem__(self, key, value):
        if type(self.ValType) == str:
            getattr(self.handler, 'write_' + self.ValType)(self.base + (self.ValLen * key), value)
        else:
            self.cache[key].replace(value)

    def replace(self, value):
        for i in range(self.Length):
            self.cache[i] = value[i]

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        self.i += 1
        if self.i > self.Length: raise StopIteration
        return self.cache[self.i - 1]

    def index_by(self, key):
        temp = dict()
        for el in self:
            if el[key] not in temp:
                temp[el[key]]=list()
            temp[el[key]].append(el)
        return temp


def get_memory_array(val_type, val_len, count):
    class TempClass(MemoryArray):
        ValType = val_type
        ValLen = val_len
        Length = count

    return TempClass
