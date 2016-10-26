# To prevent modifying the declared values
class _const:
    def __init__(self):
        # These are the defined constants that we are using.
        self.__dict__['_UNITABLE_VER']='0.8.0'
    class ConstError(TypeError): pass
    def __setattr__(self,name,value):
        if self.__dict__.has_key(name):
            print("Can't rebind const(%s)"% (name))
            raise self.ConstError
        self.__dict__[name]=value
    def __delattr__(self,name,value):
        if self.__dict__.has_key(name):
            print("Can't remove const(%s)"% (name))
            raise self.ConstError

# Add to scope
import sys
sys.modules[__name__]=_const()

'''
In the code access these like:
  import unitable.const as UNITABLE_CONST
  UNITABLE_CONST._UNITABLE_VER
'''
