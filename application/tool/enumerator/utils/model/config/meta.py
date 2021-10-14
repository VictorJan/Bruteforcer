from abc import ABC, abstractmethod
from application.utils.protocol.abstractmeta import AbstractMeta

class AbstractMetaConfig(AbstractMeta):

    def __call__(cls,*args,**kwargs):
        '''
        Dynamically recreates an instance of a Config class , the action of which is dependent
        on the instance of the first class - thus creating a new class. Based on the latter instance,
         a class is then reconstructed using the dunder __new__ in the following manner.
        The new class is being injected with __slots__, containing non-data descriptors for fetching private attributes.
        Apart from that, attrs must contain keys:"__module__","__qualname__" and other dunder-methods except
        for __dict__ and __weakref__.
        :param args:
        :param kwargs:
        :return *Config instance:
        '''

        instance = super(AbstractMetaConfig,cls).__call__(*args,**kwargs)

        if not hasattr(instance,'__slots__') or hasattr(instance,'__dict__'):
            omit=('__dict__','__weakref__')
            attrs={
                '__slots__':tuple(f'_{cls.__name__}__{key}' for key in kwargs),
                '__qualname__':cls.__name__,
                **{key:value for key,value in cls.__dict__.items() if key not in omit}
            }
            instance = super(AbstractMetaConfig,cls).__new__(AbstractMetaConfig,cls.__name__,cls.__bases__,attrs)(*args,**kwargs)

        return instance

    @abstractmethod
    def validate(self,**requirement):
        raise NotImplementedError()

    @abstractmethod
    def to_dict(self):
        raise NotImplementedError()