from abc import ABC,abstractmethod

class AbstractSubscriber(ABC):
    @abstractmethod
    def subscribe(self,topic,broker):
        raise NotImplementedError()
    @abstractmethod
    async def receive(self,topic,**data):
        raise NotImplementedError()