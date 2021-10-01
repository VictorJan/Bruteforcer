from application.tool.enumerator.utils.model.config import AbstractMetaConfig
from application.utils.protocol.descriptor import PrivateRetrieverProperty
from application.tool.enumerator.utils.model.requirement import NestedRequirement

class Config(metaclass=AbstractMetaConfig):

    def __init__(self,**data):
        '''
        Initializes a config instance , by utilizing each injected key-value pair and composing such
        instance with, given that class contains according slots and instance has no __dict__:
        - a private field and a respective value.
        - a non-data descriptor for the reconstructed class.
        :param data:
        '''
        if hasattr(self.__class__,'__slots__') and not hasattr(self,'__dict__'):
            for key,value in data.items():
                setattr(self,f'_{self.__class__.__name__}__{key}',value)
                setattr(self.__class__,key,PrivateRetrieverProperty(key))

    def validate(self,**requirement):
        '''
        Performs validation according to a provided mapping of requirements.
        This, in fact requires to pack of all of the private attributes and their respective values.
        Which is then validated by the nested requirement.
        :param requirement:dict:
        :return:
        '''

        try:requirement=NestedRequirement(**requirement)
        except TypeError as te:raise TypeError(*te.args)

        return requirement.validate(self.to_dict())

    def to_dict(self):
        '''
        Fetches all of the private attributes and returns them in a dictionary form.
        :return:
        '''
        attrs=filter(lambda item: not item[0].startswith('_') and isinstance(item[1],PrivateRetrieverProperty) ,self.__class__.__dict__.items())
        return {key: value.__get__(self) for key, value in attrs}
