from application.tool.enumerator.utils.design.pubsub.subscriber import AbstractSubscriber
from application.tool.enumerator.utils.design.pubsub.broker import AbstractSingletonBroker
from copy import deepcopy
import asyncio

class StringNotificationBroker(metaclass=AbstractSingletonBroker):
    '''
    A notification broker class - meant to ingest and transfer -> dispatch/emit and register topics, which surround/involve
    string notifications.
    '''

    def __init__(self):
        '''
        Sets up:
        - an empty hashmap for topics and subscribers, which is expected to follow the next structure:
        {topic:str : [_:AbstractSubscriber,...] , }
        - an empty hashmap for topics and notification indexes, with the following structure:
        {topic:str : int , }
        '''
        self.__topics={}
        self.__running_notification_indexes={}

    def register(self,topic,subscriber):
        '''
        Given that the types of parameters are appropriate:
        - Assigns a certain subscriber to a provided topic;
        - Binds a notification index of a provided topic to a start/running index.
        :param topic:str:
        :param subscriber:AbstractSubscriber:
        :return None:
        '''

        assert isinstance(topic,str), TypeError('Topic must be a string.')
        assert isinstance(subscriber,AbstractSubscriber), \
            TypeError('Subscriber instance must derive from a class that implements AbstractSubscriber class.')

        self.__topics[topic]=self.__topics.get(topic,[])+[subscriber]
        self.__running_notification_indexes[topic]=self.__running_notification_indexes.get(topic,0)

#    @delegator
    async def push(self,topic,**data):
        '''
        An asynchronous method which is delegated to push notifications to subscribers of a provided topic.
        In order to provide concurrency, the following steps have been taken, to implement iterations:
        - Gets a running notification index of a topic
        - Given that the index has not exhausted itself:
          - increments the notification index of a topic
          - proceeds to set a receiving task for a subscriber;
          - sets a trampoline callback to apprise more subscribers.
        - Otherwise resets the notification-queue index to a 0.
        :param topic:str:
        :param data:dict:
        :return None:
        '''
        assert isinstance(topic, str), TypeError('Topic must be a string.')
        assert all(topic in case for case in (self.__topics,self.__running_notification_indexes)), KeyError('Topic hasn\'t been registered.')
        '''
        asyncio.create_task(self._distribute(
            topic=topic,
            index=0,
            **data
        ))
        '''
        index = self.__running_notification_indexes[topic]

        if not index<len(self.__topics[topic]):
            self.__running_notification_indexes[topic]=0
        else:

            self.__running_notification_indexes[topic]+=1

            asyncio.create_task(self.__topics[topic][index].receive(topic,**data))
            if index+1<len(self.__topics[topic]):
                asyncio.create_task(self.push(topic,**data))
            else:
                self.__running_notification_indexes[topic] = 0
        #'''

    async def _distribute(self,**payload):
        required_payload = (('topic', str), ('index', int))
        assert all(payload.get(rp[0], None).__class__ is rp[1] for rp in required_payload), \
            RuntimeError(f'Provided configuration is not supported, according to a guideline : {",".join(map(str, required_payload))}')

        if (index:=payload.pop('index'))<len((subscribers:=self.__topics[(topic:=payload.pop('topic'))])):
            asyncio.create_task(subscribers[index].receive(topic,**payload))
            if index+1<len(subscribers): asyncio.create_task(self._distribute(topic=topic,index=index+1,**payload))
