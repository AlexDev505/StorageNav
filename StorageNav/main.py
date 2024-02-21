from loguru import logger

import tg
import web_app  # noqa
from app import app, config


if config.base.run_web_app:
    tg.setup_webhook()
logger.info("app started")

if __name__ == "__main__":
    if config.base.run_web_app:
        app.run(debug=True)
    else:
        tg.run_pooling()
