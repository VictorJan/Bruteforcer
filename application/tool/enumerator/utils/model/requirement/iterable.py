from application.tool.enumerator.utils.model.requirement import AbstractRequirement
from application.tool.enumerator.utils.model.requirement import TypeRequirement
from application.tool.enumerator.utils.model.requirement import MetaTypeRequirement


class IterableRequirement(AbstractRequirement):
    def __init__(self,itype,/,itemstype=None,itemsmeta=None):
        '''
        Initializes an instance of IterableRequirement, by injecting an internal type and optional type of items.
        :param itype:
        :param items:{'type':type,'meta':type}:
        '''
        if not(hasattr(itype,'__iter__')): raise TypeError('Internal type must be an iterable.')
        if not(isinstance(itype.__class__,type) or itemstype is None): raise TypeError('Internal type must be be derived from the type.')
        self.__itype = TypeRequirement(itype)
        self.__items = next((case for case in ((itemstype,TypeRequirement),(itemsmeta,MetaTypeRequirement)) if case[0] is not None),(None,None))[1]

    def validate(self,value):
        '''
        Executes iterable validation according to the following requirement:
            - A provided value must be an instance of the internal iterable type;
            -?- Given that the type of items has been provided:
                - each item is an instance of the injected items type.
        :param value:
        :return bool:
        '''
        return self.__itype.validate(value) and (all(map(lambda item:self.__items.validate(item),value)) if self.__items else True)