from application.utils.protocol.descriptor import AbstractDescriptor
from functools import partial

class awaitable(AbstractDescriptor):
    '''
    A non-data descriptor that "converts" a bounded function into a coroutine.
    '''

    def __init__(self,func):
        '''
        Initializes a descriptor with a function, which is to be assembled into a coroutine.
        :param func:
        '''
        self.__func=func

    def __get__(self,instance,owner=None):
        '''
        Prepares the functions, bounding it with an instance, providing execution to an async __call__.
        :param instance:
        :param owner:
        :return coroutine - partial __call__:
        '''
        return partial(self.__call__,instance)

    async def __call__(self,*args,**kwargs):
        '''
        Having provided an instance, executes now-bounded function as asynchronous one.
        :param args:
        :param kwargs:
        :return from self.__func:
        '''
        return self.__func(*args,**kwargs)