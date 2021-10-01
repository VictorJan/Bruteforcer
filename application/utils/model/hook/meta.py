from application.utils.design.responsibility import BaseHandler

class MetaHook(type):
    '''
    Responsible to recreate a Hook instance, by dynamically creating a new respective class, based on the provided
    filepath value for the initial instance.
    '''

    def __call__(cls, *args, **kwargs):
        '''
        Dynamically recreates an instance of a Hook class , the action of which is dependent
        on the instance of the first class - thus creating a new class. Based on the latter instance,
         a class is then reconstructed using the dunder __new__ in the following manner.
        The new class is being injected with __slots__, containing a placeholder for a trial descriptor,
        which is instantiated by a BaseHolder. Apart from that, attrs must contain keys:
        "__module__","__qualname__" and other dunder-methods except for __dict__ and __weakref__.
        :param args:
        :param kwargs:
        :return ArchiveHook instance:
        '''
        instance = super(MetaHook,cls).__call__(*args,**kwargs)

        if not hasattr(instance,'__slots__') or hasattr(instance,'__dict__'):

            if not(isinstance((source:=kwargs.get('source')),str)): raise KeyError('Source key hasn\'t been provided.')
            if not('descriptor' not in kwargs): raise KeyError('In order to recreate a class - do not provide a descriptor instance.')

            omit=('__dict__','__weakref__')
            attrs={'__slots__':f'_{cls.__name__}__trial','__qualname__':cls.__name__,
                  **{key:value for key,value in cls.__dict__.items() if key not in omit} }

            instance = super(MetaHook,cls).__new__(MetaHook,cls.__name__,cls.__bases__,attrs)(descriptor= BaseHandler().handle(name='trial',source=source))

        return instance