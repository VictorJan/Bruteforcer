class AsyncMeta(type):
    '''
    Meant to bind asynchronous behaviour to instances of a classes, that have been
    derived/created by this meta class.
    '''
    async def __call__(cls,*args,**kwargs):
        '''
        An asynchronous magic call method, which handles the creation of instances,
        acting as a middle man between the construction and the initialization,
        in this instance - enforces instances to be awaited on.
        :param args:
        :param kwargs:
        :return :coroutine:
        '''
        return super(AsyncMeta,cls).__call__(*args,**kwargs)