from abc import ABC, abstractmethod

class AbstractRequirement(ABC):

    @abstractmethod
    def validate(self,value):
        raise NotImplementedError()