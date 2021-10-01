import types

from application.tool.enumerator.utils.model.worker import AbstractWorker
from application.tool.enumerator.utils.model.worker.dispatcher import DispatcherWorker
from application.tool.enumerator.utils.model.dispatcher import StringDispatcher

from application.utils.model.hook import MetaHook

class MandateWorker(AbstractWorker):

    def __init__(self,config):
        '''
        Initializes a mandate worker with a respective configurations of:
        - a common mutable workers-queue:[AbstractWorker]
        - a hook for the dispatchers
        - submitted data :
          - requested payload
          -
        - a callback method
        hook::MetaHook,
        callback:method,
        data :
            {
            payload:str,
            running_length:int,
            suspend_length:int
            }
        }
        - common pointer to a list of workers
        - requested length of a string product
        - source of future string compounds
        - amount of workers left to set up
        - a hook for the dispatchers
        :param config:
        '''

        require_submission = ()
        required_config = (('workers', list, AbstractWorker),
                           ('hook', MetaHook),
                           ('callback',types.MethodType),
                           ('submission',dict,(
                               ('payload',str),
                               ('')
                           ))
                           )

        if not(all(config.get(rc[0], None).__class__ is rc[1] for rc in required_config)): raise \
            RuntimeError('Provided configuration is not supported, according to a guideline : {",".join(map(str, required_config))}')
        if not(all(map(lambda worker: isinstance(worker, AbstractWorker), config['workers']))): raise\
            TypeError('Workers must be be instances that derive from classes, which are implemented from the AbstractWorker class')

        self.__config=config

    async def __call__(self,config):
        '''
        An asynchronous execution of a mandate worker - proceeds to:
        - set up DispatcherWorkers
        :param config:[AbstractWorker,...]}:
        :return:
        '''

        #assings dispatcher workers
        self.__config['workers']+=[DispatcherWorker(hook=self.__config['config'],dispatcher=dispatcher) for dispatcher
                                   in StringDispatcher(self.__config['payload'],self.__config['length'])]
        #assing next mandate worker
        if (amount:=self.__config.pop('amount')-1)>0:
            self.__config['workers']+=[self.__class__(amount=amount,**config,length=self.__config['length']+1)]





