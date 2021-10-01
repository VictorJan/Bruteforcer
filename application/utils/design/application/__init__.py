from application.utils.design.application.abstract import AbstractApplication
from application.tool.abstract import AbstractTool
from application.utils.model.hook import ArchiveHook
import os

class Application(AbstractApplication):

    def __init__(self):
        self.__tool=None

    async def open(self,obj):
        assert isinstance(self.__tool, AbstractTool), TypeError('A tool hasn\'t been choosen.')
        assert isinstance(obj,str) and os.path.exists(obj) , ValueError(f'There is no such path as {obj}.')
        return await self.__tool.open(ArchiveHook(source=obj))

    @property
    def tool(self):
        return self.__tool

    @tool.setter
    def tool(self,tool):
        assert isinstance(tool, AbstractTool), TypeError('Tool must be of AbstractTool instance')
        self.__tool=tool