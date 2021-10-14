import threading

from application.tool.enumerator.utils.design.pubsub import StringNotificationBroker
from application.tool.enumerator.utils.model.dispatcher import AbstractMetaDispatcher
from application.tool.enumerator.utils.model.supply import StringSupply
from application.utils.model.hook import MetaHook
from itertools import product
from types import MethodType

import asyncio

class StringDispatcher(product, metaclass=AbstractMetaDispatcher):
    def __new__(cls,payload,amount):
        '''
        Constructs an instance , by setting up an inherited product instance, providing a string payload and a requested amount of cartesian products.
        Note: at the construction:
        - payload - is the tailing characters, a head of which is being provided at the initialization.
        - amount - is the requested amount decremented by 1, to ensure further proper length of each supply.
        :param payload:str:
        :param amount:int:
        '''
        if not isinstance(payload,str): raise TypeError('Payload must be a string.')
        if not (isinstance(amount,int) and amount>=0): raise ValueError('Amount must be a non-negative integer.')
        return super(cls,cls).__new__(cls,payload,repeat=amount)

    def __init__(self,head,length):
        '''
        Initializes the instance, by composing an one with:
        - a payload head of each supply
        - an integer length-value of each supply
        - a StringNotificationBroker - which pulls the singleton-provided instance,
        - an empty feedback queue.
        :param head:
        :param amount:
        '''
        if not (isinstance(head,str)) : raise ValueError('Head of the payload must be a string.')
        if not (isinstance(length, int)): raise ValueError('Length must be a non-negative integer.')
        self.__head = head
        self.__length = length
        self.__broker = StringNotificationBroker()
        self.__feedback_queue=[]

    def __next__(self):
        if self.__feedback_queue:
            return self.__feedback_queue.pop(0)
        return super(self.__class__,self).__next__()

    async def dispatch(self,hook,callback):
        '''
        Delegates further string verification to * StringSupplies, by setting off tasks of supplies and respective methods.
        -?- On the condition, that instance is not empty:
            - each dispatch involves compound injection, broker assignment and hands out a common hook.
              In order to provide concurrency - dispatch is called for each compound, thus behaving recursively,
              by just firing off a task to the event loop.
        :param hook :: MetaHook:
        :param callback : method:
        :return:
        '''

        if not hook.__class__.__class__ == MetaHook: raise TypeError('Hook component - must be an instance of a class instantiated by a MetaHook.')
        if not isinstance(callback,MethodType): raise TypeError('Callback must be a method.')

        if self.is_exhausted():
            return None
        else:
            compound= self.__head+(''.join(next(self)))
            string_supply = StringSupply(compound)
            string_supply.emitter.broker = self.broker
            asyncio.create_task(string_supply.checkout(hook,callback))
            asyncio.create_task(self.dispatch(hook,callback))


    def peek(self):
        '''
        Peek implementation - which allows to get the value, without exhausting the production.
        Note:the yielded tails are stored back in a feedback-queue.
        :return :
        '''
        if not self.__feedback_queue:
            try : self.__feedback_queue.append(next(self))
            except : return None
        return self.__feedback_queue[0]


    def is_exhausted(self):
        '''
        Verifies whether a dispatcher instance is empty, meaning if
        there is more cartesian product to generate, by peeking at it.
        :return bool:
        '''
        return self.peek() is None

    @property
    def broker(self):
        return self.__broker

