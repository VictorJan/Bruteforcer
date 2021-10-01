from inspect import signature

class AbstractMeta(type):

    def __init__(cls,name,bases,attrs):
        '''
        Redefines class creation - enforcing implementation of abstract methods , that has been defined below.

        Note: implementation condition - if a method has __isabstractmethod__ attribute, then an implementor class
        must contain a respective concrete method, with the same signature.
        :param name:
        :param bases:
        :param attrs:
        :return a derivative class of an AbstractMeta metaclass:
        '''
        assert all((implemetation:=cls.__dict__.get(name,None)) is not None and not hasattr(implemetation,'__isabstractmethod__') and signature(implemetation)==signature(method)
                    for name,method in cls.__class__.__dict__.items() if hasattr(method,'__isabstractmethod__')), NotImplementedError(
            f'Cannot instantiate {name} class - due to presence of not implemented,unresolved abstract methods.'
        )
        return super(AbstractMeta,cls).__init__(name,bases,attrs)