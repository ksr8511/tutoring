"""from abc import ABC"""
from abc import *

"""class Tutoring(ABC):"""
class Tutoring(metaclass=ABCMeta):
    class FileIndex:
        def __init__(self, pf, language):
            self.pf = pf
            self.language = language
            
        @classmethod
        def __get_path(cls, pf, f):
            from os.path import join
            return join('.', pf, f)

        def get_jsonorgpath(self):
            return self.__class__.__get_path(self.pf, self.pf+'_'+self.language[0:2]+'org.json')

        def get_jsonpath(self):
            return self.__class__.__get_path(self.pf, self.pf+'_'+self.language[0:2]+'.json')
            
    @classmethod
    def loopfunc(cls, t, func, *args, **kwargs):
        y = None
        while True:
            try:
                y = func(*args, **kwargs)
                break
            except Exception as err:
                print(err)
                from time import sleep
                sleep(t)
                
        return y
    
    @abstractmethod
    def collect(self):
        """"""
        
    @abstractmethod
    def get_urlarray(self, conarrayorg, unseen):
        """"""
        