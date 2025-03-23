from logging import Logger, getLogger
from fastabc import Api
from config_fastapi import Config


class LoggerMixin:
    logger: Logger = getLogger()

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj.logger = cls.logger.getChild(cls.__name__)
        return obj


class BaseResource(LoggerMixin):
    config = Config(section="api")


class BaseControl(LoggerMixin):
    config = Config(section="control")


class BaseAPI(Api, LoggerMixin):
    pass


class BaseStructures(LoggerMixin):
    pass
