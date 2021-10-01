import asyncio

from application.tool.enumerator.utils.design.pubsub.subscriber import AbstractSubscriber
from application.tool.enumerator.utils.design.pubsub.broker import AbstractSingletonBroker
import types

class StringNotificationSubscriber(AbstractSubscriber):

    def __init__(self):
        '''
        Initialization empties out the notifications.
        '''
        self.__topics=[]

    def subscribe(self,topic,broker):
        '''
        Attaches the subscriber to a provided topic, which memory-stored at the certain notification broker.
        Also stores the topic name, in the subscriptions field.
        :param topic:str :
        :param broker :: AbstractSingletonBroker :
        :return None:
        '''
        if not(isinstance(topic,str)): TypeError('Topic name must be a string.')
        if not(topic not in self.topics): raise \
            IndexError(f'The listener is already subscribed to receive notifications from {topic} topic.')
        if not(broker.__class__.__class__==AbstractSingletonBroker) : raise TypeError('Class of a broker instance had to be instantiated by the AbstractSingletonBroker.')

        self.__topics.append(topic)
        broker.register(topic,self)

    async def receive(self,topic,**data):
        '''
        Asynchronously, having received a notification - proceeds to notify the initial supplier,
        by using a provided/included callback.
        :param topic:str:
        :param **data:
        :return None:
        '''
        if not(topic in self.__topics): raise \
            IndexError(f'The listener is not subscribed to receive notifications from {topic} topic.')
        if not((callback:=data.pop('callback',False))): raise KeyError('A callback has\'t been provided.')
        if not(isinstance(callback,types.MethodType)): raise TypeError('A callback must be a method.')
        asyncio.create_task(callback(self,topic=topic,**data))

    @property
    def topics(self):
        '''
        Retrieves a tuple of topics, that the listener has subscribed to.
        :return tuple(topic:str,...):
        '''
        return tuple(self.__topics)