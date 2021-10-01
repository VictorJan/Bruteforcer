from application.utils.protocol.abstractmeta import AbstractMeta
from abc import abstractmethod

class AbstractMetaHandler(AbstractMeta):
    def __setattr__(cls,name,value):
        '''
        Sets value to a class-level attribute, prioritizing data descriptors over simple assignments.
        Also , permits derivatives to change the attribute value.
        :param name:
        :param value:
        :return:
        '''
        if (attr:=cls.__dict__.get(name)):
            if (dunder_set:=getattr(attr,'__set__',False)):
                dunder_set(cls,value)
            else:
                super(AbstractMetaHandler,cls).__setattr__(name,value)
        else:
            carrier=next((case for case in cls.__mro__ if name in case.__dict__))
            super(AbstractMetaHandler,(carrier or cls)).__setattr__(name,value)

    @abstractmethod
    def handle(self,**case):
        raise NotImplementedError()