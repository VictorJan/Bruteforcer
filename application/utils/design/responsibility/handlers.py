from application.utils.design.responsibility import AbstractMetaHandler
from application.utils.protocol.descriptor import ClassProperty

from application.utils.protocol.descriptor import ArchiveTrialDescriptor
from application.utils.model.trial import ZIPTrial,RARTrial

import re

class BaseHandler(metaclass=AbstractMetaHandler):
    '''
    Meant to implement a default way to handle cases - to transfer/hand down them to the next handler.
    '''

    __consecutive=0

    def handle(self,**case):
        '''
        Hands downs a case to the next/consecutive handler - if there is one.
        This method is meant to be overridden, however it could be invoked by instances
        of classes that implement such abstract class.
        :param case:
        :return:
        '''
        if not(issubclass(self.__class__, BaseHandler)): raise TypeError('This method shall only be called by instances of implementor classes.')
        if (successor:=self.__class__.consecutive)<len(derivatives:=BaseHandler.__subclasses__()):
            self.__class__.consecutive += 1
            return derivatives[successor]().handle(**case)
        raise StopIteration('Handlers have been exhausted/enumerated.')

    @ClassProperty
    def consecutive(cls):
        return cls.__consecutive

    @consecutive.setter
    def consecutive(cls, value):
        if not(isinstance(value,int)): raise TypeError('Value must be an integer.')
        if not(value<len(cls.__subclasses__())): raise ValueError('Must not overflow the current amount of handlers.')
        cls.__consecutive=value


class RARHandler(BaseHandler):
    '''
    Handles the rar extension cases - preparing a respective instance of classes deriving from AbstractTrialDescriptor and AbstractTrialArchive.
    '''
    def handle(self,**case):
        '''
        Meant to handle RAR file cases - by instantiating and returning a respective descriptor instance ,
        given the proper circumstances and proper requisites. Otherwise proceeds to hand down the handling.
        :param case:string, matching a rar regex pattern:
        :return a ArchiveTrialDescriptor , injected with a respective Trial instance - RARTrial / hands down the handling:
        '''
        return ArchiveTrialDescriptor(case['name'],RARTrial(case['source'])) if all(necessary in case for necessary in ('name','source')) and \
        re.fullmatch('.+\.rar',case['source']) else super(RARHandler, self).handle(**case)

class ZIPHandler(BaseHandler):
    '''
    Handles the zip extension cases - preparing a respective instance of classes deriving from AbstractTrialDescriptor and AbstractTrialArchive.
    '''
    def handle(self,**case):
        '''
        Meant to handle ZIP file cases - by instantiating and returning a respective descriptor instance ,
        given the proper circumstances and proper requisites. Otherwise proceeds to hand down the handling.
        :param case:string, matching a zip regex pattern:
        :return a ArchiveTrialDescriptor , injected with a respective Trial instance - ZIPTrial / hands down the handling:
        '''
        return ArchiveTrialDescriptor(case['name'],ZIPTrial(case['source'])) if all(necessary in case for necessary in ('name','source')) and \
        re.fullmatch('.+\.zip',case['source']) else super(ZIPHandler, self).handle(**case)