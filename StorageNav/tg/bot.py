import time

from telebot import TeleBot

from app import config
from .exceptions import MyExcHandler


bot = TeleBot(
    config.tg_bot.token,
    threaded=False,
    parse_mode="HTML",
    exception_handler=MyExcHandler(),
)


def setup_webhook() -> None:
    bot.remove_webhook()
    time.sleep(0.1)
    bot.set_webhook(
        f"{config.tg_bot.webhook.host}/{config.tg_bot.webhook.secret_key}",
        max_connections=1,
    )


def run_pooling():
    bot.remove_webhook()
    bot.infinity_polling()


__all__ = ["bot", "config", "setup_webhook", "run_pooling"]
