from abc import ABC, abstractmethod
class Builder(ABC):
    @property
    @abstractmethod
    def product(self):
        raise NotImplementedError()
