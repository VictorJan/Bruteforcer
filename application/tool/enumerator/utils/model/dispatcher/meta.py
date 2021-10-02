from application.utils.protocol.abstractmeta import AbstractMeta
from abc import abstractmethod

class AbstractDispatcher(AbstractMeta):

    __distribution={}

    def __call__(cls, payload, length=1):
        '''
        Distributes dispatchers for each character in a provided payload to run concurrently.
        Based on the distribution hashmap , with the following structure:
        { (payload,length):tuple : running index:int }
        For each instantiation based on the provided payload, returns a respective dispatcher, in following manner:

        - fetches a running index for the (payload,length) key from the hashmap.

        -?- If the key doesn't exist - set a default one with a value of 0
        -?> Otherwise index is assigned with an appropriate running value.

        -?- Given that the retrieved index hasn't exhausted the payload:
            - construct a dispatcher instance with the full payload,decrementing the length;
            - initialize an instance with the head as a payload , and the full length;
            - increment the index value.
        -?> Otherwise pop the distribution key out of the hashmap and apprise a StopIteration error.

        :param payload:str:
        :param length:int:
        :return:
        '''
        if not(isinstance(payload,str)): raise TypeError('Payload must be a string.')
        if not(isinstance(length,int)): raise TypeError('Length must be an integer.')


        index=cls.__distribution.setdefault((key:=(payload,length)),0)

        if index < len(payload):
            instance = cls.__new__(cls, payload, length-1)
            instance.__init__(payload[index], length)
            cls.__distribution[key]+=1
        else:
            cls.__distribution.pop(key)
            raise StopIteration

        return instance


    @abstractmethod
    async def dispatch(self,hook,callback):
        raise NotImplementedError()

    @abstractmethod
    def is_empty(self):
        raise NotImplementedError()