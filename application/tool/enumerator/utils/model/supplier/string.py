import types

from application.tool.enumerator.utils.model.supplier import AbstractSupplier

from application.tool.enumerator.utils.design.pubsub import StringNotificationSubscriber
from application.tool.enumerator.utils.design.pubsub import StringNotificationBroker

from application.tool.enumerator.utils.model.config import Config
from application.utils.model.requirement import NestedRequirement,TypeRequirement,IterableRequirement,MetaTypeRequirement
from application.tool.enumerator.utils.model.worker import AbstractWorker,MandateWorker

from application.utils.model.hook import MetaHook

import asyncio


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
        Hands down string augment to concurrent executions of workers, by firing off a delegate method,
        providing a starter-config, which at first contains an empty worker-queue, in order to instantiate
        a starter-MandateWorker with the latter config. Then ,in order to get the concurrency going the
        worker is appended to the worker-queue in the config.
        Consequently, the starter-config has the following structure:
        {
        workers-queue:[MandateWorker]
        hook::MetaHook,
        callback:method,
        submission:
            {
            payload:str,
            running_length:int,
            suspension_length:int
            }
        }
        :param hook:: MetaHook:
        :return password:str/None, failure:int:
        '''
        if not hook.__class__.__class__ == MetaHook: raise TypeError('Hook component - must be an instance of a class instantiated by a MetaHook.')
        numeral = '1234567890'

        self.listener.subscribe('password_feedback',StringNotificationBroker())
        starter_config=Config(
            workers=[],
            hook=hook,
            callback=self._callback,
            submission=dict(
                payload='aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ'+numeral,
                running_length=3,
                suspension_length=5
            )
        )
        starter_worker = MandateWorker(starter_config)

        starter_config.workers.append(starter_worker)

        asyncio.create_task(self._delegate(starter_config))

        return await self.__product,self.__failure

    async def _delegate(self,config):
        '''
        Asynchronously manages/delegates execution of workers - provided from a MandateConfig:
        Given that the worker-queue is not empty, proceeds to:
        - set a task on the event loop for the very first worker of a queue
        - set up a callback/task to itself - to provide looping
        Thus , it could be inferred , that the event loop callbacks, would look like this:
        -_delegate(...)
        -Worker(...)()
        -_delegate(...)
        -Worker(...)()
        ...

        This would work,only if the Abstract Meta Dispatcher , keeps on providing different String Dispatchers,
        based on the same payload and length, until it exhausts itself based on the payload -> providing a None.
        :param config::AbstractConfig:
        :return:
        Note: each worker is responsible to assign other workers to the worker/job-queue.
        '''

        if not isinstance(config.__class__,Config.__class__): raise TypeError(f'A config must be an instance of a class that implements AbstractConfig.')

        if not config.validate(
            workers=IterableRequirement(list,AbstractWorker),
            hook=MetaTypeRequirement(MetaHook),
            callback=TypeRequirement(types.MethodType),
            submission=NestedRequirement(
                payload=TypeRequirement(str),
                running_length=TypeRequirement(int),
                suspension_length=TypeRequirement(int)
            )
        ): raise KeyError('A provided config is invalid.')

        if config.workers:
            asyncio.create_task(config.workers.pop(0)())
            asyncio.create_task(self._delegate(config))


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
        if not procurer is self.listener: raise AttributeError('A procurer must be a listener of the supplier.')
        if not all(data.get(rc[0], None).__class__ is rc[1] for rc in required_data):
            raise RuntimeError(f'Provided configuration is not supported, according to a guideline : {",".join(map(str, required_data))}')

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
