from application.tool.enumerator.utils.model.supply import AbstractSupply
from application.tool.enumerator.utils.design.pubsub import StringNotificationPublisher
from application.utils.model.hook import MetaHook
import asyncio

class StringSupply(AbstractSupply):
    def __init__(self,payload:str):
        '''
        Initialize a string supply - composing of a concrete emitter:StringNotificationPublisher.
        '''
        if not(isinstance(payload,str)): raise TypeError('Payload must be a string.')
        self.__emitter=StringNotificationPublisher()
        self.__payload=payload

    async def checkout(self,hook, callback):
        '''
        Using the hook/hook - proceeds to delegate the verification of the composite payload.
        After which - publishes a feedback notification, using the following structure:
        { "password": :str: , "state": :bool: }
        In order to provide access restrictions/security - the Thread locks during the trial value
        assignment and validation obtainment.
        :param hook :: MetaHook :
        :param callback : method:
        :return:
        '''
        if not(hook.__class__.__class__ == MetaHook): raise TypeError('Hook component - must be an instance of a class instantiated by a MetaHook.')
        try:
            hook.trial = self.__payload
            trial = await hook.trial
            self.emitter.publish('password_feedback', callback=callback, password=self.__payload, state=trial[1])
        except BlockingIOError:
            return

    @property
    def emitter(self):
        return self.__emitter


