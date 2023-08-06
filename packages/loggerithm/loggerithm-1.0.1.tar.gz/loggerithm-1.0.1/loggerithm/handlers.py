from typing import *
import sys
import pathlib
import datetime
import re

_COLOURCHAR = re.compile('\x1b\\[[0-9;]+?m')



def STDOUT(line: str):
    sys.stdout.write(f'{line}\n')
    sys.stdout.flush()


def STDERR(line: str):
    sys.stderr.write(f'{line}\n')
    sys.stderr.flush()


class FILE():
    def __init__(self, dir: pathlib.Path, file: Optional[str] = None):
        if (not isinstance(dir, pathlib.Path)):
            raise(TypeError('Argument `dir` must be of type `pathlib.Path{{is_dir}}`'))
        elif (not dir.is_dir()):
            raise(TypeError('Argument `dir` must be of type `pathlib.Path{{is_dir}}`'))
        elif (not (file == None or isinstance(file, str))):
            raise(TypeError('Argument `file` must be of type `optional(str)`'))
        if (file == None):
            file = f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")}.log'
        self.file = dir / file
        with open(self.file, 'w') as f:
            f.write('')
    def __call__(self, line: str):
        with open(self.file, 'a') as f:
            f.write(_COLOURCHAR.sub('', line) + '\n')
