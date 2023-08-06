from typing import Tuple, Callable, Union

import re
import datetime
from coloured import *

__version__ = '0.1.0'



class LoggerMethod():
    def __init__(self, name: str, level: int = 0, fmt: Tuple[FormatString] = (), parent = None):
        if (not isinstance(name, str)):
            raise(TypeError('Argument `name` must be of type `str`'))
        elif (not isinstance(level, int)):
            raise(TypeError('Argument `level` must be of type `int`'))
        elif ((not isinstance(fmt, tuple)) or (not all([callable(i) for i in fmt]))):
            raise(TypeError('Argument `fmt` must be of type `tuple(coloured.FormatString)'))
        elif (re.fullmatch(r'[a-z]+', name) == None):
            raise(ValueError('Argument `name` must match pattern `[a-z]+`'))
        elif (name in ['log']):
            raise(TypeError('Argument `name` must not be a blacklisted method name'))
        elif (level < 0):
            raise(ValueError('Argument `level` must be at least 0'))

        self.name = name
        self.level = level
        self.fmt = fmt
        self.parent = parent


    def __call__(self, message: str):
        self.parent.LOG(self, message)



class LoggerTarget():
    def __init__(self, target: Callable, fmt: Union[str, FormatString] = '{time} - {method} : {message}'):
        if (not callable(target)):
            raise(TypeError('Argument `target` must be callable'))
        elif (not (isinstance(fmt, str) or isinstance(fmt, FormatString))):
            raise(TypeError('Argument `fmt` must be of type `str` or `FormatString`'))

        self.target = target
        self.fmt = fmt



class Logger():
    def __init__(self):
        self.methods = []
        self.targets = []
        self.methodlength = 0


    def LOG(self, method: LoggerMethod, message: str):
        if (not isinstance(method, LoggerMethod)):
            raise(TypeError('Argument `method` must be of type `LoggerMethod`'))
        elif (not isinstance(message, str)):
            raise(TypeError('Argument `message` must be of type `str`'))

        if (not method in self.methods):
            raise(TypeError('Argument `method` must be a valid method'))

        resmethod = method.name.ljust(self.methodlength)
        for func in method.fmt:
            resmethod = func(resmethod)

        for func in method.fmt:
            message = func(message)

        now = datetime.datetime.now()
        time = {}
        timeslots = ['a', 'A', 'w', 'd', 'b', 'B', 'm', 'y', 'Y', 'H', 'I', 'p', 'M', 'S', 'f', 'z', 'Z', 'j', 'U', 'W', 'c', 'x', 'X']
        for slot in timeslots:
            time[f't_{slot}'] = now.strftime(f'%{slot}')

        for target in self.targets:
            target.target(
                target.fmt.format(
                    time    = str(now),
                    method  = resmethod,
                    message = message,
                    **time
                )
            )


    def newmethod(self, name: str, level: int = 0, fmt: Tuple[FormatString] = ()):
        if (not isinstance(name, str)):
            raise(TypeError('Argument `name` must be of type `str`'))
        elif (not isinstance(level, int)):
            raise(TypeError('Argument `level` must be of type `int`'))
        elif (name in self.methods):
            raise(ValueError(f'Logging level `{name.upper()}` already exists'))

        loggermethod = LoggerMethod(name, level, fmt, parent=self)
        setattr(self, name.upper(), loggermethod)
        self.methods.append(loggermethod)

        length = len(name)
        if (length > self.methodlength):
            self.methodlength = length


    def newtarget(self, target: Callable, fmt: Union[str, FormatString] = '{time} - {method} : {message}'):
        self.targets.append(LoggerTarget(target, fmt))


def new(name: str = None):
    logger = Logger()
    if (isinstance(name, str)):
        globals()[name] = logger
    elif (name != None):
        raise(TypeError('Argument `name` must be of type `str` or `None`'))
    return(logger)



if (__name__ == '__main__'):
    logger = new()

    logger.newmethod('trace', level=5, fmt=(Style.faint,))
    logger.newmethod('debug', level=10, fmt=(ColourFg.default,))
    logger.newmethod('info', level=20, fmt=(ColourFg.cyan, Style.faint))
    logger.newmethod('success', level=25, fmt=(ColourFg.green, Style.bold))
    logger.newmethod('warning', level=30, fmt=(ColourFg.yellow,))
    logger.newmethod('error', level=40, fmt=(ColourFg.red, Style.bold))
    logger.newmethod('critical', level=50, fmt=(ColourBg.white, ColourFg.red, Style.bold))

    def loghandler(line: str):
        print(line)
    logger.newtarget(target=loghandler)

    logger.LOG(logger.TRACE, 'You have been traced')
    logger.LOG(logger.DEBUG, 'No bugs allowed')
    logger.LOG(logger.INFO, 'You have been informed that...')
    logger.LOG(logger.SUCCESS, 'When at first you don\'t succeed, try and try again')
    logger.LOG(logger.WARNING, 'This is your final warning!')
    logger.LOG(logger.ERROR, 'This is an error message')
    logger.LOG(logger.CRITICAL, 'Something went horribly wrong!')
