import logging
import logging.handlers
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod

LOGVALUE = {
    'NOTSET': 0,
    'DEBUG': 10,
    'INFO': 20,
    'WARN': 30,
    'WARNING': 30,
    'ERROR': 40,
    'CRITICAL': 50,
    'FATAL': 50
}


class LogValue(Enum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARN = 30
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    FATAL = 50


@dataclass
class Logger:
    name: str
    logDir: str
    logName: str
    maxBytes: int
    backupCount: int
    mode: str
    level: str
    stream: bool
    level_set: dict = field(default_factory=dict)

    def __init__(self,
                 name: str,
                 logDir: str,
                 logName: str = 'sample.log',
                 maxBytes: int = 5242990,
                 backupCount: int = 5,
                 mode: str = 'a',
                 level: str = 'INFO',
                 stream: bool = True
                 ):
        self.name = name
        self.logDir = logDir
        self.logName = logName
        self.maxBytes = maxBytes
        self.backupCount = backupCount
        self.mode = mode
        self.level = level
        self.stream = stream
        self.level_set = LOGVALUE

    def with_suffix(self, logName):
        return str(Path(logName).with_suffix('.log'))

    def set_logdir(self):
        return Path.home()


@dataclass
class Settings(ABC):
    level_set: dict = field(init=True, default_factory=LOGVALUE)
    name: str = ''
    logName: str = 'sample.log'
    logDir: str = None
    maxBytes: int = 5200
    backupCount: int = 5
    mode: str = 'a'
    level: str = 'INFO'

    @abstractmethod
    def set_logdir(self):
        return Path.home()



class RotatingLog_Old(Settings):
    def __init__(self, name: str, logName='sample', logDir=None,
                 maxBytes=5242990, backupCount=5, mode='a', level='INFO'):
        """ Creates an instance for each new Rotating Logger"""
        logDir = logDir if logDir else self.set_logdir()
        self.settings = Settings(name=name, logName=logName, logDir=logDir,
                                 maxBytes=maxBytes, backupCount=backupCount, mode=mode,
                                 level=level, level_set=LOGVALUE)
        self.formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)-8s %(message)s')
        self.file_handler = logging.handlers.RotatingFileHandler(
            Path.joinpath(Path(self.settings.logDir) / f"{self.settings.logName}.log"),
            mode=self.settings.mode, maxBytes=self.settings.maxBytes,
            backupCount=self.settings.backupCount)
        self.file_handler.setFormatter(self.formatter)

        stream_formatter = logging.Formatter('%(levelname)-8s: %(message)s')
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.stream_formatter)

        self.logger = logging.getLogger(self.settings.name).setLevel(self.settings.level)
        self.logger = logging.getLogger(self.settings.name).addHandler(self.file_handler)
        self.logger = logging.getLogger(self.settings.name).addHandler(self.stream_handler)

    def getLogger(self, name=None):
        return logging.getLogger(self.settings.name) if not name else self.addLogger(name)

    def addLogger(self, name):
        self.logger = logging.getLogger(name).setLevel(self.settings.level)
        self.logger = logging.getLogger(name).addHandler(self.file_handler)
        self.logger = logging.getLogger(name).addHandler(self.stream_handler)
        return logging.getLogger(name)

    def set_logdir(self):
        return super().set_logdir()


class RotatingLog(Logger):
    def __init__(self, name: str, logName='sample.log', logDir=None,
                 maxBytes=5242990, backupCount=5, mode='a', level='INFO', stream=True):
        """ Creates an instance for each new Rotating Logger"""
        logDir = logDir if logDir else self.set_logdir()
        logName = self.with_suffix(logName)
        super().__init__(name=name, logName=logName, logDir=logDir, maxBytes=maxBytes,
                         backupCount=backupCount, mode=mode, level=level, stream=stream)

        self.formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)-8s %(message)s')
        self.file_handler = logging.handlers.RotatingFileHandler(
            Path.joinpath(Path(self.logDir) / self.logName),
            mode=self.mode, maxBytes=self.maxBytes, backupCount=self.backupCount)
        self.file_handler.setFormatter(self.formatter)

        if self.stream:
            self.stream_formatter = logging.Formatter('%(levelname)-8s: %(message)s')
            self.stream_handler = logging.StreamHandler()
            self.stream_handler.setFormatter(self.stream_formatter)

        self.logger = logging.getLogger(self.name).setLevel(self.level)
        self.logger = logging.getLogger(self.name).addHandler(self.file_handler)
        if self.stream:
            self.logger = logging.getLogger(self.name).addHandler(self.stream_handler)

    def getLogger(self, name=None):
        return logging.getLogger(self.name) if not name else self.addLogger(name)

    def addLogger(self, name):
        self.logger = logging.getLogger(name).setLevel(self.settings.level)
        self.logger = logging.getLogger(name).addHandler(self.file_handler)
        if self.stream:
            self.logger = logging.getLogger(name).addHandler(self.stream_handler)
        return logging.getLogger(name)
