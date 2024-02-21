from __future__ import annotations

import typing as ty

from .bot import bot
from loguru import logger


if ty.TYPE_CHECKING:
    from telebot.types import Message


@bot.message_handler(commands=["start"])
def start(message: Message):
    logger.opt(colors=True).debug(
        f"<e>{message.from_user.username}</e> (id: <r>{message.from_user.id}</r>) "
        "called <y>start</y> command"
    )
    bot.reply_to(message, "Hi!")
