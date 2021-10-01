from abc import ABC,abstractmethod
class AbstractPublisher(ABC):
    @abstractmethod
    def publish(self,topic,**data):
        raise NotImplementedError()
    @property
    @abstractmethod
    def broker(self):
        raise NotImplementedError()

    @broker.setter
    @abstractmethod
    def broker(self,other):
        raise NotImplementedError()