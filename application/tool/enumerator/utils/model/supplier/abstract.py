from abc import ABC,abstractmethod

class AbstractSupplier(ABC):
    @abstractmethod
    async def supply(self,hook):
        raise NotImplementedError()

    @abstractmethod
    async def _callback(self, procurer, **data):
        raise NotImplementedError()

    @abstractmethod
    async def _delegate(self,config):
        raise NotImplementedError()