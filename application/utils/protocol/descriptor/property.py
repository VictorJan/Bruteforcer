from application.utils.protocol.descriptor import AbstractDescriptor

class ClassProperty(AbstractDescriptor):
    '''
    A class property data descriptor.
    '''
    def __init__(self,fget=None,fset=None):
        '''
        Initialize a get and a set unbound functions.
        :param fget:
        :param fset:
        '''
        self.__fget=fget
        self.__fset=fset

    def __get__(self,instance,owner):
        '''
        Returns execution of the get function.
        :param instance:
        :param owner:
        :return:
        '''
        return self.__fget(owner)

    def __set__(self,cls,value):
        '''
        Executes the set descriptor, binding a function to a class.
        :param cls:
        :param value:
        :return:
        '''
        assert isinstance(cls,type), TypeError('Cls parameter must be a class type.')
        self.__fset(cls,value)

    def setter(self,fset):
        '''
        Returns an instance of a Data ClassProperty Descriptor.
        :param fset:
        :return:
        '''
        return self.__class__(self.__fget,fset)