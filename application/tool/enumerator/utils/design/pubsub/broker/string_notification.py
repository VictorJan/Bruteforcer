from application.tool.enumerator.utils.design.pubsub.subscriber import AbstractSubscriber
from application.tool.enumerator.utils.design.pubsub.broker import AbstractSingletonBroker
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

        if not(isinstance(topic,str)): raise TypeError('Topic must be a string.')
        if not(isinstance(subscriber,AbstractSubscriber)): raise \
            TypeError('Subscriber instance must derive from a class that implements AbstractSubscriber class.')

        self.__topics[topic]=self.__topics.get(topic,[])+[subscriber]
        self.__running_notification_indexes[topic]=self.__running_notification_indexes.get(topic,0)

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
        if not(isinstance(topic, str)): raise TypeError('Topic must be a string.')
        if not all(topic in case for case in (self.__topics,self.__running_notification_indexes)): raise KeyError('Topic hasn\'t been registered.')


        if not (index:=self.__running_notification_indexes[topic])<len(self.__topics[topic]):
            self.__running_notification_indexes[topic]=0
        else:
            self.__running_notification_indexes[topic]+=1
            asyncio.create_task(self.__topics[topic][index].receive(topic,**data))

            if index+1<len(self.__topics[topic]):
                asyncio.create_task(self.push(topic,**data))
            else:
                self.__running_notification_indexes[topic] = 0