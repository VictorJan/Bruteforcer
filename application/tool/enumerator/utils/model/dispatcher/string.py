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
        Constructs an instance , by setting up an inherited instance, providing a string payload and a requested amount of cartesian products.
        :param payload:str:
        :param amount:int:
        '''
        assert isinstance(payload,str), TypeError('Payload must be a string.')
        assert isinstance(amount,int) and amount>0, TypeError('Amount must be an integer, which is greater than 0.')
        return super(cls,cls).__new__(cls,payload,repeat=amount-1)

    def __init__(self,payload,amount):
        '''
        Initializes the instance, by composing an instance of a StringNotificationBroker - which would return the singleton,
        and an empty feedback queue.
        :param payload:
        :param amount:
        '''
        self.__broker=StringNotificationBroker()
        self.__payload=payload
        self.__feedback_queue=[]

    async def dispatch(self,hook,callback):
        '''
        Delegates further string verification to * StringSupplies, by setting off tasks of supplies and respective methods.
        Each dispatch involves compound injection, broker assignment and hands out a common hook.
        In order to provide concurrency - dispatch is called for each compound, thus this requires to behave recursively,
        ,by firing a task , given that the is more compounds to generate.
        :param hook :: MetaHook:
        :param callback : method:
        :return:
        '''

        assert hook.__class__.__class__ == MetaHook, TypeError('Hook component - must be an instance of a class instantiated by a MetaHook.')
        assert isinstance(callback,MethodType), TypeError('Callback must be a method.')

        if self.is_empty():
            return None
        else:
            compound = ''.join(self.__feedback_queue.pop(0) if self.__feedback_queue else next(self))
            string_supply = StringSupply(compound)
            string_supply.emitter.broker = self.broker
            asyncio.create_task(string_supply.checkout(hook,callback))
            asyncio.create_task(self.dispatch(hook,callback))

    async def __delegate(self,index,**config):
        if index<len(self.__payload):
            compound = ''.join(self.__feedback_queue.pop(0) if self.__feedback_queue else next(self))
            print(self.__payload[index]+compound)
            string_supply = StringSupply(self.__payload[index]+compound)
            string_supply.emitter.broker = self.broker
            asyncio.create_task(string_supply.checkout(config['hook'], config['callback']))
            asyncio.create_task(self.__delegate(index+1,**config))





    def is_empty(self):
        if not (last:=next(self,False)) or (not last and not self.__feedback_queue):
            return True
        self.__feedback_queue.insert(0,last)
        return False

    @property
    def broker(self):
        return self.__broker

