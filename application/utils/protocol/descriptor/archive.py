from application.utils.protocol.descriptor import AbstractTrialDescriptor
from application.utils.model.trial import AbstractArchiveTrial

class ArchiveTrialDescriptor(AbstractTrialDescriptor):

    def __init__(self,name:str,trial:AbstractArchiveTrial):
        '''
        Initializes the ArchiveTrialDescriptor object, by injecting an AbstractArchiveTrial instance as a trial.
        :param trial:AbstractArchiveTrial:
        '''
        assert isinstance(trial,AbstractArchiveTrial), TypeError('The trial must an instance of AbstractArchiveTrial.')
        self.__trial=trial
        self.__name=name
        self.__locked=False

    async def __get__(self,instance,owner):
        '''
        Given that a trial value is pending , if state hasn't been locked:
        Retrieves the placeholder value, then anticipates for an async validation task to finish.
        Should validation be successful - we proceed to set up the locked out state
        and the trial outcome at the private attribute.
        At last the outcome is provided to the caller.
        :param instance - an object that has invoked the descriptor:
        :param owner - the owner of the object:
        :return tuple(trial value:str , state:bool):
        '''
        assert (value:=getattr(self,f'_{self.__class__.__name__}__placeholder',None)) is not None, ValueError('Trial hasn\'t been set up.')

        getter=(instance,f'_{instance.__class__.__name__}__{self.__name}')

        if not self.__locked and (validation:=await self.__trial.verify(value)):
            self.__locked=True
            setattr(*getter,(value,validation))
        return getattr(*getter)


    def __set__ (self,instance,value):
        '''
        Sets up a value placeholder - if the trial hasn't been locked out,
        otherwise a BlockingIOError is apprised.
        :param instance:
        :param value:
        :return:
        '''
        assert isinstance(value,str) , TypeError('Value parameter must be a string instance.')
        if not self.__locked:
            self.__placeholder=value
        else:
            raise BlockingIOError('Trial has been locked.')

