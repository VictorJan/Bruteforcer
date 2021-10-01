from application.tool.abstract import AbstractTool
from application.tool.enumerator.utils.model.supplier import StringSupplier
from application.utils.model.hook import MetaHook

class EnumeratorTool(AbstractTool):

    async def open(self,obj):
        '''
        Delegates further string augment to * StringDispatches, by setting off threads of dispatching objects and respective methods, after which awaits for a notification.
        Each dispatch is handed out with a common hook.
        :param hook:: MetaHook:
        :return:
        '''
        assert obj.__class__.__class__ == MetaHook, TypeError(
            'Object component - must be an instance of a class instantiated by a MetaHook.')
        result = await StringSupplier().supply(obj)
        return f'Password has {"not " if result[0] is None else ""} been found {" - {} .".format(result[0]) if result[0] is not None else "."}' \
               f'Amount of failed attempts is {result[1]}.'