from application.utils.protocol.abstractmeta import AbstractMeta
from abc import abstractmethod


class AbstractSingletonBroker(AbstractMeta):

    __instance=None

    def __call__(cls,*args,**kwargs):
        '''
        Integration of the singleton state.
        :param args:
        :param kwargs:
        :return:
        '''
        assert (mcls:=cls.__class__)==AbstractSingletonBroker, TypeError('Class that wishes to create an instance must have been instantiated by the AbstractSingletonBroker.')

        if mcls.__instance is None:
            mcls.__instance = super(mcls,cls).__call__(*args,**kwargs)

        return mcls.__instance

    @abstractmethod
    def register(self,topic,subscriber):
        raise NotImplementedError()

    @abstractmethod
    def push(self,topic,**data):
        raise NotImplementedError()