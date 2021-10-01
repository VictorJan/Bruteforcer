from application.utils.model.hook import MetaHook
from application.utils.protocol.descriptor import AbstractTrialDescriptor

class ArchiveHook(metaclass=MetaHook):

    def __init__(self,**kwargs):
        '''
        Dynamically initializes an instance of ArchiveHook class, in the following way.
        If kwargs contain a descriptor instance and appropriate slots have been defined, by the meta class - proceed
        to set the descriptor attribute at the class level. Nonetheless, a private trial attribute is still set up as
        a default tuple of (None,False).
        :param kwargs - expecting : 1.{"source":str} ~> 2.{"descriptor":AbstractTrialDescriptor}:
        '''


        if isinstance(kwargs.get('descriptor',None),AbstractTrialDescriptor) and getattr(self, '__slots__','') == f'_{self.__class__.__name__}__trial':

            setattr(self.__class__,'trial',kwargs['descriptor'])

        self.__trial = (None,False)