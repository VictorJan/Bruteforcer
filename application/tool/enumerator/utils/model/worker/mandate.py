import types

from application.tool.enumerator.utils.model.worker.dispatcher import DispatcherWorker
from application.tool.enumerator.utils.model.dispatcher import StringDispatcher

from application.tool.enumerator.utils.model.config import Config
from application.tool.enumerator.utils.model.requirement import NestedRequirement,TypeRequirement,IterableRequirement,MetaTypeRequirement
from application.tool.enumerator.utils.model.worker import AbstractWorker


from application.utils.model.hook import MetaHook

class MandateWorker(AbstractWorker):

    def __init__(self,config):
        '''
        Initializes a mandate worker with a respective config which follows the following guideline:
            - a common mutable workers-queue:[AbstractWorker]
            - a hook for the dispatchers
            - a callback method
            - submitted data:
                - a requested payload
                - a running length
                - a suspension length
        :param config::AbstractConfig:
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

        self.__config=config
        self.__next=None

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

        try:
            self.__config.workers.append(DispatcherWorker(Config(
                hook=self.__config.hook,
                callback=self.__config.callback,
                dispatcher=StringDispatcher(self.__config.submission['payload'],self.__config.submission['running_length'])
            )))
            self.__config.workers.append(self)
        except StopIteration:
            pass

        if self.__next is None and not (next_length:=self.__config.submission['running_length']+1)>self.__config.submission['suspension_length']:
            self.__next = MandateWorker(Config(
                **{
                    **self.__config.to_dict(),
                    'submission': {
                        **self.__config.submission,
                        'running_length': next_length
                    }
                }
            ))
            self.__config.workers.append(self.__next)



