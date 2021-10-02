import threading

from application.tool.enumerator.utils.design.pubsub import StringNotificationBroker
from application.tool.enumerator.utils.model.dispatcher import AbstractDispatcher
from application.tool.enumerator.utils.model.supply import StringSupply
from application.utils.model.hook import MetaHook
from itertools import product
from types import MethodType

import asyncio

class StringDispatcher(product,metaclass=AbstractDispatcher):
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
        if not (isinstance(amount,int) and amount>1): raise ValueError('Amount must be an integer, which is greater than 1.')
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
        if not (isinstance(head,str) and len(head)==1) : raise ValueError('Head of the payload must be a single character string.')
        if not (isinstance(length, int) and length > 0): raise ValueError('Length must be an integer, which is greater than 0.')
        self.__head = head
        self.__length = length
        self.__broker = StringNotificationBroker()
        self.__feedback_queue=[]

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

        if self.is_empty():
            return None
        else:
            compound = self.__head+(''.join(self.__feedback_queue.pop(0) if self.__feedback_queue else next(self)))
            string_supply = StringSupply(compound)
            string_supply.emitter.broker = self.broker
            asyncio.create_task(string_supply.checkout(hook,callback))
            asyncio.create_task(self.dispatch(hook,callback))


    def is_empty(self):
        '''
        Verifies whether a dispatcher instance is empty, meaning if there is more cartesian product to generate.
        The yielded tails are stored back in a feedback-queue, at the back.
        :return bool:
        '''
        if not (last:=next(self,False)) or (not last and not self.__feedback_queue):
            return True
        self.__feedback_queue.append(last)
        return False

    @property
    def broker(self):
        return self.__broker

