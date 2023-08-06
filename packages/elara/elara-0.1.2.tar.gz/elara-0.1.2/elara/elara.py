'''
Copyright (c) 2021, Saurabh Pujari
All rights reserved.

This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree.
'''
import os
import json
from .elarautil import Util

class Elara():

    from .strings import (setnx, append, getset, mget, mset, msetnx, slen)
    from .lists import (lnew, lpush, lextend, lindex, lrange, lrem, lpop, llen, lappend, lexists, linsert)
    from .hashtables import (hnew, hadd, haddt, hget, hpop, hkeys, hvals, hexists, hmerge)
    from .shared import (retmem, retdb, retkey, commit, exists, exportdb, exportkeys, exportmem, securedb, updatekey)

    def __init__(self, path, commitdb, key_path = None):
        self.path = os.path.expanduser(path)
        self.commitdb = commitdb 

        # Since key file is generated first, invalid token error for pre existing open dbs

        # Load the database key
        if not key_path==None:
            new_key_path = os.path.expanduser(key_path)
            if os.path.exists(new_key_path):
                file = open(new_key_path, 'rb')
                self.key = file.read()
                file.close()
            else:
                self.key = None
        else:
            self.key = None

        # Load the data
        if os.path.exists(path):
            self._load()
        else:
            self.db = {}

    def _load(self):
        if self.key:
            self.db = Util.readAndDecrypt(self)
        else:
            self.db = Util.readJSON(self)

    def _dump(self):
        if self.key:
            Util.encryptAndStore(self) # Enclose in try-catch
        else:
            Util.storeJSON(self)

    def _autocommit(self):
        if self.commitdb:
            self._dump()
    
    def set(self, key, value):
        if isinstance(key, str):
            self.db[key] = value
            self._autocommit()
            return True
        else:
            raise Exception
    
    def get(self, key):
        try:
            return self.db[key]
        except KeyError:
            return None
    
    def rem(self, key):
        del self.db[key]
        self._autocommit()
        return True
    
    def clear(self):
        self.db = {}
        self._autocommit()
        return True