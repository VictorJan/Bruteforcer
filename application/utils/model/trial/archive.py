import asyncio

from application.utils.model.trial import AbstractArchiveTrial
import zipfile
import rarfile

class RARTrial(AbstractArchiveTrial):
    _extension = 'rar'
    async def verify(self,value):
        '''
        An async method - performs password verification, by trying to open and read the compressed rar file.
        :param value - password string:
        :return True or False:
        '''

        if not isinstance(value, str): raise ValueError('Value parameter must a string.')
        with rarfile.RarFile(self.filepath) as f:
            try:
                f.read(f.namelist()[0],pwd=value)
                return True
            except rarfile.BadRarFile:
                return True
            except RuntimeError as re:
                if 'Bad password' in str(re):
                    return False
                raise re


class ZIPTrial(AbstractArchiveTrial):
    _extension = 'zip'
    async def verify(self,value):
        '''
        An async method - performs password verification, by trying to open and read the compressed zip file.
        :param value - password string:
        :return bool:
        '''

        if not isinstance(value,str) : raise ValueError('Value parameter must a string.')

        with zipfile.ZipFile(self.filepath) as file:
            try:
                f = file.open(file.infolist()[-1], pwd=value.encode())
                f.read()
            except RuntimeError as re:
                if self._exception_pattern(re.args[0]):
                    return False
                raise re
            except zipfile.BadZipfile as bz:
                return False
        return True

