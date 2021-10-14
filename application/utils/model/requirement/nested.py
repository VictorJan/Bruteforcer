from application.utils.model.requirement import AbstractRequirement
from application.utils.model.requirement import TypeRequirement


class NestedRequirement(AbstractRequirement):
    def __init__(self,**initial):
        '''
        Initializes an instance of IterableRequirement, by composing itself with:
            - an internal type requirement of a dictionary.
            - an empty requirement dictionary.
        Given there are initial requirements - proceed to add them.
        :return None:
        '''

        self.__itype = TypeRequirement(dict)
        self.__requirements={}

        for key,requirement in initial.items():
            self.add(key,requirement)

    def add(self,key,requirement):
        '''
        Inserts a requirement (an instance of concrete *Requirement class), binding it to a string key.
        :param key:
        :param requirement:
        :return:
        '''
        if not(isinstance(key, str)): raise TypeError('A requirement key must be a string.')
        if not(isinstance(requirement,AbstractRequirement)): raise TypeError(
            'A requirement must be an instance of a concrete class that derived from the AbstractRequirement.')

        self.__requirements.update({key:requirement})

    def validate(self,value):
        '''
        Executes nested validation according to the following requirement:
            - A provided value must be an instance of the internal type, which is a dict;
            - Searches for any case when:
                - a required key is absent.
                - data, which is bounded to a key is invalid, according to a respective requirement from the guidelines.
                Otherwise - data assigned to necessary keys has been validated.
            - Verifies absence of any unnecessary data, by reasoning the lengths of:
                the guidelines-map and the provided value-map.
        :param value:dict:
        :return bool:
        '''
        return self.__itype.validate(value) and \
            not any(map(lambda req: not (req[1].validate(obj) if (obj:=value.get(req[0],False)) is not False else obj), self.__requirements.items())) and \
               len(value)==len(self.__requirements)