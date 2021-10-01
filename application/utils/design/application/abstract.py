from abc import ABC, abstractmethod

class AbstractApplication(ABC):

    @abstractmethod
    async def open(self,obj):
        raise NotImplementedError()

    @property
    @abstractmethod
    def tool(self):
        raise NotImplementedError()

    @tool.setter
    @abstractmethod
    def tool(self,strategy):
        raise NotImplementedError()