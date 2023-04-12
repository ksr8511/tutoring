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
            from pathlib import Path
            """return join('.', pf, f)"""
            return join(Path.home(), 'jupyter', 'tutoring', pf, f)
            
        def get_jsonorgpath(self):
            return self.__class__.__get_path(self.pf, self.pf+'_'+self.language[0:2]+'org.json')

        def get_jsonpath(self):
            return self.__class__.__get_path(self.pf, self.pf+'_'+self.language[0:2]+'.json')
            
    def __init__(self, pf, language):
        self.language = language
        """self.fileindex = self.__class__.FileIndex(self.__class__.pf, self.language)"""
        """self.fileindex = self.__class__.FileIndex(self.__class__.__get_pf(), self.language)"""
        self.fileindex = self.__class__.FileIndex(pf, self.language)
        
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
        
    @abstractmethod
    def remove_log(self):
        """"""
        