from application.utils.design.builder import Builder
from application.utils.design.application import Application
from application.tool.abstract import AbstractTool

class ApplicationBuilder(Builder):

    def __init__(self):
        self.__reset()

    @property
    def tool(self):
        '''
        A tool property - responsible to return a core component of an application - alluding the strategy.
        :return self.__tool:
        '''
        if not(isinstance(self.__application.tool, AbstractTool)): raise TypeError(
            'An application hasn\'t been built.')
        return self.__application.tool

    @tool.setter
    def tool(self,strategy):
        '''
        Sets and ensures that the provided strategy instance is valid.
        :param strategy:
        :return None:
        '''
        if not(isinstance(strategy,AbstractTool)): raise TypeError('Strategy must an instance of an AbstractTool class.')
        self.__application.tool=strategy

    @property
    def product(self):
        '''
        Provides an application, with a respective algorithm.
        :return self.__application:
        '''
        if not(isinstance(self.__application.tool,AbstractTool)): TypeError('An application hasn\'t been built.')
        product=self.__application
        self.__reset()
        return product

    def __reset(self):
        '''
        Resets the builder.
        :return None:
        '''
        self.__application=Application()



