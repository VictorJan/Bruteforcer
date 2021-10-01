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

    def __get__(self,instance,owner=None):
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
        if not isinstance(cls,type): raise TypeError('Cls parameter must be a class type.')
        self.__fset(cls,value)

    def setter(self,fset):
        '''
        Returns an instance of a Data ClassProperty Descriptor.
        :param fset:
        :return:
        '''
        return self.__class__(self.__fget,fset)



class PrivateRetrieverProperty(AbstractDescriptor):
    '''
    A property used to retrieve private fields.
    '''

    def __init__(self,name):
        '''
        Initialize a name of a private attribute.
        :param fget:
        :param fset:
        '''
        if not isinstance(name,str): raise TypeError('Name of a private attribute must be a string.')
        self.__name=name

    def __get__(self,instance,owner=None):
        '''
        Fetches value of the private attribute.
        :param instance:
        :param owner:
        :return:
        '''
        return getattr(instance,f'_{instance.__class__.__name__}__{self.__name}',None)
