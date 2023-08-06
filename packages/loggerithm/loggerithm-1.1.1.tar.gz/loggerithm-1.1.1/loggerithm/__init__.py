from typing import Tuple, Callable, Union, Optional

import re
import datetime
import coloured
from coloured import *
import pathlib
import toml

import loggerithm.handlers

__version__ = '1.1.1'



class LoggerMethod():
    def __init__(self, name: str, level: int = 0, label: Optional[str] = None, fmt: Tuple[FormatString, ...] = (), parent = None):
        if (not isinstance(name, str)):
            raise(TypeError('Argument `name` must be of type `str`'))
        elif (not isinstance(level, int)):
            raise(TypeError('Argument `level` must be of type `int`'))
        elif (not isinstance(label, str)):
            raise(TypeError('Argument `label` must be of type `optional(str)'))
        elif ((not isinstance(fmt, tuple)) or (not all([callable(i) for i in fmt]))):
            raise(TypeError('Argument `fmt` must be of type `tuple(coloured.FormatString, ...)'))
        elif (re.fullmatch(r'[a-z0-9]+', name) == None):
            raise(ValueError('Argument `name` must match pattern `[a-z0-9]+`'))
        elif (name in ['log']):
            raise(TypeError('Argument `name` must not be a blacklisted method name'))
        elif (level < 0):
            raise(TypeError('Argument `level` must be at least 0'))

        self.name = name
        self.logginglevel = level
        self.label = label
        self.fmt = fmt
        self.parent = parent


    def setlevel(self, level: int):
        if (level < 0):
            raise(ValueError('Argument `level` must be at least 0'))

        self.logginglevel = level


    def __call__(self, message: str):
        self.parent.LOG(self, message)


    def __repr__(self):
        return(f'<loggerithm.LoggerMethod(name={self.name}, level={self.logginglevel})>')



class LoggerTarget():
    def __init__(self, target: Callable, level: int = 0, fmt: Union[str, FormatString] = '{time} - {method} : {message}'):
        if (not callable(target)):
            raise(TypeError('Argument `target` must be callable'))
        elif (not isinstance(level, int)):
            raise(TypeError('Argument `level` must be of type `int`'))
        elif (not (isinstance(fmt, str) or isinstance(fmt, FormatString))):
            raise(TypeError('Argument `fmt` must be of type `union(str, FormatString)`'))

        self.target = target
        self.logginglevel = level
        self.fmt = fmt


    def setlevel(self, level: int):
        if (level < 0):
            raise(ValueError('Argument `level` must be at least 0'))

        self.logginglevel = level


    def __repr__(self):
        return(f'<loggerithm.LoggerTarget(target={self.target}, level={self.logginglevel})>')



class Logger():
    def __init__(self, loadfromconfig: Optional[pathlib.Path] = None):
        if (not (loadfromconfig == None or isinstance(loadfromconfig, pathlib.Path))):
            raise(TypeError('Argument `loadfromconfig` must be of type `optional(pathlib.Path)`'))
        self.methods = []
        self.targets = []
        #self.labellength = 0
        self.logginglevel = 0
        if (loadfromconfig != None):
            data    = toml.load(loadfromconfig).get('loggerithm', {})
            methods = data.get('methods', {})
            for key in methods.keys():
                method = methods[key]
                format = [getattr(getattr(coloured, k), v) for k,v in [(i.split('.')[0], i.split('.')[1]) for i in method.get('format', [])]]
                self.newmethod(
                    key,
                    level = method.get('level', 0),
                    label = method.get('label', None),
                    fmt   = tuple(format)
                )
            targets = data.get('target', [])
            for target in targets:
                self.newtarget(
                    getattr(loggerithm.handlers, target.get('target')),
                    level = target.get('level', 0),
                    fmt   = target.get('format', '{time} - {method} : {message}')
                )
            self.setlevel(data.get('level', 0))
            


    def LOG(self, method: LoggerMethod, message: str):
        if (not isinstance(method, LoggerMethod)):
            raise(TypeError('Argument `method` must be of type `LoggerMethod`'))
        elif (not isinstance(message, str)):
            raise(TypeError('Argument `message` must be of type `str`'))

        if (not method in self.methods):
            raise(TypeError('Argument `method` must be a valid method'))

        #resmethod = method.label.ljust(self.labellength)
        resmethod  = method.label
        for func in method.fmt:
            resmethod = func(resmethod)

        for func in method.fmt:
            message = func(message)

        now = datetime.datetime.now()
        time = {}
        timeslots = ['a', 'A', 'w', 'd', 'b', 'B', 'm', 'y', 'Y', 'H', 'I', 'p', 'M', 'S', 'f', 'z', 'Z', 'j', 'U', 'W', 'c', 'x', 'X']
        for slot in timeslots:
            time[f't_{slot}'] = now.strftime(f'%{slot}')

        def stylefunc(groups):
            return(''.join([f'\x1b[{i}m' for i in getattr(getattr(coloured, groups.group(1)), groups.group(2))('').parts[0].colours]))

        if (method.logginglevel >= self.logginglevel):
            for target in self.targets:
                if (method.logginglevel >= target.logginglevel):
                    target.target(
                        re.sub('\\{(ColourFg|ColourBg|Style|Reset)\\.([a-z]+)\\}', stylefunc, target.fmt).format(
                            time    = str(now),
                            method  = resmethod,
                            message = message,
                            **time
                        )
                    )


    def newmethod(self, name: str, level: int = 0, label: Optional[str] = None, fmt: Tuple[FormatString, ...] = ()):
        if (name in self.methods):
            raise(ValueError(f'Logging method `{name.upper()}` already exists'))

        loggermethod = LoggerMethod(name, level, label, fmt, parent=self)
        setattr(self, name.upper(), loggermethod)
        self.methods.append(loggermethod)

        #length = len(label)
        #if (length > self.labellength):
        #    self.labellength = length


    def newtarget(self, target: Callable, level: int = 0, fmt: Union[str, FormatString] = '{time} - {method} : {message}'):
        self.targets.append(LoggerTarget(target, level, fmt))
        return(self.targets[-1])


    def setlevel(self, level: int):
        if (level < 0):
            raise(ValueError('Argument `level` must be at least 0'))

        self.logginglevel = level


    def __repr__(self):
        return(f'<loggerithm.Logger(methods={len(self.methods)}, targets={len(self.targets)}, level={self.logginglevel})>')



def new(name: str = None, loadfromconfig: Optional[pathlib.Path] = None):
    logger = Logger(loadfromconfig=loadfromconfig)
    if (isinstance(name, str)):
        globals()[name] = logger
    elif (name != None):
        raise(TypeError('Argument `name` must be of type `str` or `None`'))
    return(logger)
