from application.tool.enumerator.utils.design.decorator import ToolDecorator

from time import time
class TimeItToolDecorator(ToolDecorator):
    '''
    A TimeIt decorator.
    '''

    def __init__(self, wrapee):
        if not( isinstance(wrapee,ToolDecorator.__base__)): raise TypeError(
            'The component must be derived from a class that implements AbstractTool.')
        self.__wrapee = wrapee

    async def open(self,obj):
        '''
        Calculates how much time has elapsed.
        :param obj:
        :return:
        '''
        start = time()
        outcome = await self.__wrapee.open(obj)
        return outcome,f'Time taken : {(time() - start)} s. has elapsed.'