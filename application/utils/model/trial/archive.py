import asyncio

from application.utils.model.trial import AbstractArchiveTrial
import zipfile
import subprocess
from unrar import rarfile

class RARTrial(AbstractArchiveTrial):
    _extension = 'rar'
    async def verify(self,value):
        '''
        An asynchronous function meant to perform password validation for the rar case.
        Verification invokes an unrar subprocess, using the following command, which tests a provided
        archive based on the inserted password-value.
        unrar t -p{value} {self.filepath}
        :param value - password string:
        :return True or False:
        '''

        if not isinstance(value, str): raise ValueError('Value parameter must a string.')

        process_args = ['unrar', 't', f'-p{value}', self.filepath]
        process = await asyncio.create_subprocess_shell(' '.join(process_args), stdout=asyncio.subprocess.PIPE,
                                                        stderr=asyncio.subprocess.PIPE)
        stoud,_ = await process.communicate()

        return True if 'All OK' in stoud.decode() else False


class ZIPTrial(AbstractArchiveTrial):
    _extension = 'zip'
    async def verify(self,value):
        '''
        An async method - performs password verification, by trying to open and read the compressed zip file,
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

