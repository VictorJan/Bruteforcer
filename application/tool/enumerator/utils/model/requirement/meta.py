from application.tool.enumerator.utils.model.requirement import AbstractRequirement

class MetaTypeRequirement(AbstractRequirement):
    def __init__(self,imtype):
        '''
        Initializes an instance of MetaTypeRequirement, by injecting an internal meta type.
        :param imtype:
        '''
        if not(isinstance(imtype,type)): raise TypeError('Internal mtype must be be derived from the type.')
        self.__imtype=imtype

    def validate(self,value):
        '''
        Executes type validation according to the following requirement:
        Class of a provided value must be an instance of the internal meta type.
        :param value:
        :return bool:
        '''
        return isinstance(value.__class__,self.__imtype)