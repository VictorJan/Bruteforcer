from application.utils.protocol.abstractmeta import AbstractMeta
from abc import abstractmethod

class AbstractDispatcher(AbstractMeta):

    def __call__(cls, payload, length=1):
        '''
        Distributes dispatchers/workers among each character to run concurrently.
        :param payload:
        :param length:
        :return:
        '''
        assert isinstance(payload,str), TypeError('Payload must be a string.')
        assert isinstance(length,int), TypeError('Length must be an integer.')

        index,workers=0,[]
        while index<len(payload):
            workers.append(cls.__new__(payload,length-1))
            workers[index].__init__(payload[index],length)
            index+=1
        return workers


    @abstractmethod
    async def dispatch(self,hook,callback):
        raise NotImplementedError()