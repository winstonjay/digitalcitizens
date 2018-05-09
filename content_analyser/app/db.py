# -*- coding: utf-8 -*-
import os
import pickle


class Cache(object):
    '''
    Pretty much a wrapper around a dictionary that saves stuff to memory.
    '''
    def __init__(self, path, data={}):
        self.path = path
        if not os.path.exists(path):
            print("A new db will be created:", path)
            self.data = {}
            return
        # we already have a db so load the data from that.
        with open(self.path, "rb") as fp:
            print("Loading ache: ", path)
            self.data = DictUnpickler(fp).load()

    def __setitem__(self, key, item):
        self.data[key] = item
        with open(self.path, 'wb') as fp:
            pickle.dump(self.data, fp)

    def __getitem__(self, key):
        return self.data.get(key, None)

    def __contains__(self, key):
        return key in self.data

    def __len__(self):
        return len(self.data)


class DictUnpickler(pickle.Unpickler):
    '''Unpickle but assert we are reading a dictionary.'''

    def find_class(self, module, name):
        # Only allow the builtin dict type
        if module == "builtins" and name == 'dict':
            return getattr(builtins, name)
        # Forbid everything else.
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
                                     (module, name))