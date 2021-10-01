from abc import ABC,abstractmethod

class AbstractTool(ABC):
    @abstractmethod
    async def open(self,obj):
        raise NotImplementedError()
