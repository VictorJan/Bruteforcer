import threading
import types

from application.tool.enumerator.utils.model.supplier import AbstractSupplier
from application.tool.enumerator.utils.design.pubsub import StringNotificationSubscriber
from application.tool.enumerator.utils.model.dispatcher import StringDispatcher
from application.tool.enumerator.utils.model.config import Config
from application.tool.enumerator.utils.model.requirement import NestedRequirement,TypeRequirement,IterableRequirement,MetaTypeRequirement

from application.tool.enumerator.utils.model.worker import AbstractWorker

from application.utils.model.hook import MetaHook

import asyncio

from threading import Thread,active_count

class StringSupplier(AbstractSupplier):

    def __init__(self):
        '''
        Initialize a string supplier - composing of a concrete listener:StringNotificationSubscriber.
        Perform a composition of a response:Event - an event placeholder for the event loop to simmer down.
        '''
        self.__listener=StringNotificationSubscriber()
        self.__product=asyncio.Future()
        self.__failure=0

    async def supply(self,hook):
        '''
        Hands down string augment to concurrent execution of workers, by firing off a delegate method,
        providing a respective configuration - a worker-queue, with a single starter MandateWorker, which assigns
        other Mandate and Dispatcher workers.
        Important to denote that , the Mandate workers are injected with the following config:
        {
        workers-queue:[AbstractWorker]
        hook::MetaHook,
        callback:method,
        submission :
            {
            payload:str,
            running_length:int,
            suspend_length:int
            }
        }

        Delegates further string augment to * StringDispatches, by setting off async tasks of
        dispatch method of instantiated instances. Each dispatch is handed out with a common hook.
        :param hook:: MetaHook:
        :return password:str/None, failure:int:
        '''
        assert hook.__class__.__class__ == MetaHook, TypeError('Hook component - must be an instance of a class instantiated by a MetaHook.')
        config_payload=dict(
            workers=[],
            hook=hook,
            callback=self._callback,
            submission=dict(
                payload='aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ',
                running_length=3,
                suspend_length=5
            )
        )

        '''
        asyncio.create_task(self._delegate(
            hook,
            workers=[MandateWorker()]
            workers=1,
            length=4,
            topic='password_feedback',
            payload='abcdefg'  # 'aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYz'[::2]
        ))
        '''
        '''
        asyncio.create_task(self._delegate(
            hook,
            #workers=AbstractWorker()
            workers=1,
            length=4,
            topic='password_feedback',
            payload='abcdefg'#'aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYz'[::2]
        ))
        '''

        return await self.__product,self.__failure

    async def _delegate(self,config):
        '''
        Asynchronously manages/delegates execution of workers - provided from a MandateConfig:
        Given that the worker-queue is not empty, proceeds to:
        - set a task on the event loop for the very first worker of a queue
        - set up a callback/task to itself - to provide looping
        Thus , it could be inferred , that the event loop callbacks, would look like this:
        -Worker(...)()
        -_delegate(...)
        -Worker(...)()
        ...

        or
        1.MandateWorker($1)() ---> worker-queue:[3,4]
        2._delegate(...)
        3.DispatcherWorker(StringDispatcher)
        4.MandateWorker($1)
        4

        This would work,only if the Abstract Meta Dispatcher , keeps on providing different String Dispatchers,
        based on the same payload and length, until it exhausts itself based on the payload -> providing a None.



        :param config:Config{
        workers:[AbstractWorker,...] - a FIFO queue
        }
        :return:
        Note: each worker is responsible to assign other workers to the worker/job-queue.
        '''

        if not isinstance(config.__class__,Config.__class__): raise TypeError(f'A config must be an instance of a class that implements AbstractConfig.')

        if config.validate(
            workers=IterableRequirement(list, AbstractWorker),
            hook=MetaTypeRequirement(MetaHook),
            callback=TypeRequirement(types.MethodType),
            submission=NestedRequirement(
                payload=TypeRequirement(str),
                running_length=TypeRequirement(int),
                suspend_length=TypeRequirement(int)
            )
        ): raise KeyError('A provided config is invalid.')

        if config.workers:
            asyncio.create_task(config.workers.pop(0)())
            asyncio.create_task(self._delegate(config))



        '''
        Config(
                    workers=config.workers,
                    hook=config.hook,
                    callback=config.callback,
                    submission=config.submission
                )
        if config['workers']:
            worker=config['workers'].pop(0)()
            asyncio.create_task(self._delegate(**config))
            #set 
        '''

    async def _callback(self, procurer, **data):
        '''
        An asynchronous callback - meant to be invoked by a subscriber complement, of which the current supplier is composed.
        Sequentially, product is set up / Future is ensured , if:
        - provided notification has a password with a valid state;
        or
        - there is no more tasks on the event loop,except the main one.
        Otherwise - the failure counter is incremented.
        :param procurer:
        :param data:
        :return:
        '''

        required_data = (('topic',str), ('password', str), ('state', bool))
        assert procurer is self.listener , AttributeError('A procurer must be a listener of the supplier.')
        assert all(data.get(rc[0], None).__class__ is rc[1] for rc in required_data), \
            RuntimeError(f'Provided configuration is not supported, according to a guideline : {",".join(map(str, required_data))}')

        print('at callback:',data)
        if data['state']:
            self.__product.set_result(data['password'])
        elif len(asyncio.all_tasks())==1:
            self.__product.set_result(None)
        else:
            self.__failure+=1

    @property
    def listener(self):
        '''
        Returns the agglomerate listener.
        :return listener:StringNotificationSubscriber:
        '''
        return self.__listener
