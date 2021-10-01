from abc import ABC,abstractmethod

class AbstractWorker(ABC):

    @abstractmethod
    def __init__(self,**config):
        raise NotImplementedError()

    @abstractmethod
    async def __call__(self):
        raise NotImplementedError()