from application.tool.abstract import AbstractTool

class ToolDecorator(AbstractTool):
    async def open(self,obj):
        '''
        Delegates execution to the decorated instance.
        :param obj:
        :return:
        '''
        if not( hasattr(self,f'_{self.__class__.__name__}__wrapee')) : raise AttributeError('ToolDecorator must have a private "wrapee" attribute.')
        return self.__wrapee.open(self,obj)

