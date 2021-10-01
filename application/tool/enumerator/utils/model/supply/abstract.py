from abc import ABC,abstractmethod

class AbstractSupply(ABC):

    @abstractmethod
    async def checkout(self,hook,callback):
        raise NotImplementedError()