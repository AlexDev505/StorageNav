import threading

from loguru import logger

import tg
import web_app  # noqa
from app import app, config


if config.tg_bot.enabled and config.tg_bot.webhook.enabled:
    tg.setup_webhook()

logger.info("app started")

if __name__ == "__main__":
    if config.tg_bot.enabled:
        if config.tg_bot.webhook.enabled:
            app.run()
        elif config.web_app.enabled:
            t = threading.Thread(target=tg.run_pooling)
            t.daemon = True
            t.start()
        else:
            tg.run_pooling()
    if config.web_app.enabled:
        if not config.tg_bot.webhook.enabled:
            app.run()
