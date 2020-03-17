import logging
import os
from time import sleep
from uuid import UUID

from pysesame2 import Sesame

logger = logging.getLogger(__name__)

SESAME_DEVICE_UUID = os.getenv("SESAME_DEVICE_UUID")
SESAME_APIKEY = os.getenv("SESAME_APIKEY")
device_id = UUID(SESAME_DEVICE_UUID)


def unlock() -> bool:
    logger.info("Move into SESAME API Request process")
    sesame = Sesame(device_id, SESAME_APIKEY)
    status = sesame.get_status()
    logger.info(status)
    if not status["locked"]:
        logger.info("Not locked.")
        return True

    task = sesame.async_unlock()
    while task.pooling() is False:
        logger.info("Processing...")
        sleep(1)
    if task.is_successful:
        logger.info("Unlock Succeed!")
        return True
    else:
        logger.error(f"Failed: {task.error()}")
        return False
