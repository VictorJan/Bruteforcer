import asyncio

from application.utils.model.trial import AbstractArchiveTrial
from application.utils.protocol.descriptor.asynchoronous import awaitable
import zipfile

import subprocess

class RARTrial(AbstractArchiveTrial):
    _extension = 'rar'

    async def verify(self,value):
        '''
        An async method - performs password verification, by trying to open and read the compressed rar file.
        In order to enhance execution speed - instead of .open/.read - utilizes:
        A subprocess popen call, which internally creates a child process,
        that writes output to a respective stdout file descriptor, with the help of a cli command:
        'unrar p -idq -p[value] [self.filepath]' - which only outputs data if the passcode is valid.
        In order to enhance the speed execution :
            -?- if the instantiated file descriptor for the stdout is over 100, runs synchronously.
            -> otherwise sets a task on the event loop , to run concurrently.
        :param value - password string:
        :return True or False:
        '''
        if not isinstance(value, str): raise ValueError('Value parameter must a string.')
        cmd=['unrar', 'p','-idq',f'-p{value}', self.filepath]
        process=subprocess.Popen(cmd,stdout=-1,stderr=-1)
        if process.stdout.fileno()>100:process.wait()
        else: await asyncio.create_task(awaitable(process.wait)())
        return bool(process.stdout.read(1))

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

