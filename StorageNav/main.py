from loguru import logger

import tg
import web_app  # noqa
from app import app, config


if __name__ == "__main__":
    logger.info("app started")

    if config.base.run_web_app:
        tg.setup_webhook()
        app.run(debug=True)
    else:
        tg.run_pooling()
