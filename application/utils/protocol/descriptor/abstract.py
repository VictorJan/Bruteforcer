from abc import ABC,abstractmethod

class AbstractDescriptor(ABC):
    @abstractmethod
    def __get__(self,instance,owner=None):
        raise NotImplementedError()

class AsyncAbstractDescriptor(AbstractDescriptor):
    @abstractmethod
    async def __get__(self,instance,owner=None):
        raise NotImplementedError


class AbstractTrialDescriptor(AbstractDescriptor):

    @abstractmethod
    def __init__(self,trial):
        raise NotImplementedError()

    @abstractmethod
    def __set__(self, instance, value):
        raise NotImplementedError