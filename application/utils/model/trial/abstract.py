from abc import ABC,abstractmethod
import os,re

class AbstractTrial(ABC):
    @abstractmethod
    def verify(self,value):
        raise NotImplementedError()

class AbstractArchiveTrial(AbstractTrial):

    _exception_pattern = lambda cls,exception: bool(re.fullmatch('Bad password for [fF]ile.*',exception))
    _extension='(?:rar|zip)'

    def __init__(self,filepath):
        if not(os.path.exists(filepath)): raise ValueError(f'{filepath} does not exist.')
        if not(re.fullmatch(f'.*\.{self._extension}',filepath)) : raise ValueError('Provided filepath parameter must allude to an appropriate archive.')
        self.__filepath=filepath

    @property
    def filepath(self):
        return self.__filepath