from application.utils.model.requirement import AbstractRequirement

class TypeRequirement(AbstractRequirement):
    def __init__(self,itype):
        '''
        Initializes an instance of TypeRequirement, by injecting an internal type.
        :param itype:
        '''
        if not(isinstance(itype.__class__,type)): raise TypeError('Internal type must be be derived from the type.')
        self.__itype=itype

    def validate(self,value):
        '''
        Executes type validation according to the following requirement:
        A provided value must be an instance of the internal type.
        :param value:
        :return bool:
        '''
        return isinstance(value,self.__itype)