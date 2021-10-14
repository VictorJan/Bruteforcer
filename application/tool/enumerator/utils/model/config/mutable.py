from application.tool.enumerator.utils.model.config import AbstractMetaConfig
from application.utils.protocol.descriptor import PrivateDataDescriptor

from application.utils.model.requirement import AbstractRequirement,NestedRequirement,TypeRequirement

class MutableConfig(metaclass=AbstractMetaConfig):

    def __init__(self,requirements,**data):
        '''
        Initializes a mutable config instance , by utilizing each injected key-value pair and composing such
        instance with a PrivateDataDescriptor providing a private name and a respective AbstractRequirement
        provided in the "requirements":dict argument, only if such argument contains keys, that correspond to
        the names of soon-to-be private attributes, and values of such entries must be of AbstractRequirement implementation.

        The latter actions take place, given that class contains according slots and instance has no __dict__:
        - a private field and a respective value.
        - a data descriptor /w a respective requirement.
        :param data:
        '''

        if hasattr(self.__class__,'__slots__') and not hasattr(self,'__dict__'):

            requirements_guide = NestedRequirement(**{
                key: TypeRequirement(AbstractRequirement)
                for key in data
            })

            if not requirements_guide.validate(requirements):
                raise RuntimeError('Provided requirements either don\'t correspond '
                                   'to injected data or some requirements '
                                   'aren\'t concrete instances of AbstractRequirement class.')

            for key,value in data.items():
                setattr(self,f'_{self.__class__.__name__}__{key}',value)
                setattr(self.__class__, key, PrivateDataDescriptor(key,requirements[key]))

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
        attrs=filter(lambda item: not item[0].startswith('_') and isinstance(item[1], PrivateDataDescriptor), self.__class__.__dict__.items())
        return {key: value.__get__(self) for key, value in attrs}
