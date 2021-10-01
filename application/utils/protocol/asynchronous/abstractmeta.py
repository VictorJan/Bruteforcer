from application.utils.protocol.abstractmeta import AbstractMeta
from application.utils.protocol.asynchronous.meta import AsyncMeta

class AbstractAsyncMeta(AsyncMeta,AbstractMeta):
    '''
    A mixin class - meant to complement both async and abstract meta behaviours.
    '''

    pass