from loguru import logger
from telebot import ExceptionHandler


class MyExcHandler(ExceptionHandler):
    def handle(self, exception):
        logger.exception(exception)
