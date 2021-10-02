import asyncio

from application.tool.enumerator.utils.model.worker import AbstractWorker
from application.tool.enumerator.utils.model.dispatcher import AbstractDispatcher

from application.tool.enumerator.utils.model.requirement import TypeRequirement,MetaTypeRequirement
from application.tool.enumerator.utils.model.config import Config
from application.utils.model.hook import MetaHook
import types

class DispatcherWorker(AbstractWorker):

    def __init__(self,config):
        '''
        Initializes a dispatcher worker with a respective config which follows the following guideline:
            - a string-dispatcher instance
            - a hook for the dispatcher
            - a callback method
        :param config::AbstractConfig:
        '''

        if not isinstance(config.__class__, Config.__class__): raise TypeError(
            f'A config must be an instance of a class that implements AbstractConfig.')

        if not config.validate(
                dispatcher=MetaTypeRequirement(AbstractDispatcher),
                hook=MetaTypeRequirement(MetaHook),
                callback=TypeRequirement(types.MethodType),
        ): raise KeyError('A provided config is invalid.')

        self.__config = config

    async def __call__(self):
        '''
        An asynchronous execution of a mandate worker, based on the composing config,
        proceeds to do the following:
        -?- tries to:
            - fetch a string-dispatcher instance from the distribution, based on
            payload and length values from the config.
            - appends a DispatcherWorker instance to the end of a worker-queue in the config,
            having provided a separate config for the dispatcher-worker ,injecting:
                - a hook;
                - a callback;
                - the dispatcher instance itself.
            - prepends the same MandateWorker to the queue - which means that the current worker can
        -?> Given that the instantiation of the distribution has raised the StopIteration error, alluding that:
            - all string-dispatchers , based on the latter payload and running length, have been exhausted.
        -?- at last, if the current worker hasn't already assigned the next MandateWorker
         and the next running length is not about to suspend:
            - set up the next MandateWorker, composing one with a separate config, which includes:
                - the common worker-queue, the hook and the callback
                - a submission hash-map, containing the next running length with the same payload and suspension.
            - insert the latter MandateWorker to the common worker-queue.
        :return:
        '''
        asyncio.create_task(self.__config.dispatcher.dispatch(self.__config.hook,self.__config.callback))