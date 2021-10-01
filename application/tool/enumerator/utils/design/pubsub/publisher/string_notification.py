from application.tool.enumerator.utils.design.pubsub.publisher import AbstractPublisher
from application.tool.enumerator.utils.design.pubsub.broker import AbstractSingletonBroker
import asyncio
from copy import deepcopy

class StringNotificationPublisher(AbstractPublisher):

    def __init__(self):
        self.__broker=None

    def publish(self,topic,**data):
        '''
        Apprises a notification, related to a certain topic , which would consist of provided data.
        By setting a coroutine wrapped in a Task, on a current event loop.
        :param topic:str:
        :param data:dict:
        :return None:
        '''
        assert isinstance(topic,str), TypeError('An topic name must be a string.')
        assert self.broker is not None , NotImplementedError('A broker hasn\'t been assinged , consequently one shall not be able to publish a notification.')
        asyncio.create_task(self.broker._distribute(topic=topic,index=0,**data))

    @property
    def broker(self):
        '''
        Retrieves current broker value.
        :return self.__broker:None/:: AbstractSingletonBroker :
        '''
        return self.__broker
    @broker.setter
    def broker(self,other):
        '''
        Assings a broker to a publisher.
        :param other::AbstractSingletonBroker :
        :return None:
        '''
        assert other.__class__.__class__ == AbstractSingletonBroker, TypeError(
            'Class of a broker instance had to be instantiated by the AbstractSingletonBroker.')
        self.__broker=other