import binascii
import errno
import logging
import time

import nfc

import sesame_api

SLEEP_SEC = 1


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class SesameNFCReader:
    def validate_idm(self, idm: str) -> bool:
        logger.info(idm)
        return True

    def on_connect(self, tag: nfc.tag.Tag) -> None:
        logger.info(tag)
        idm = binascii.hexlify(tag.identifier).decode().upper()
        if self.validate_idm(idm):
            sesame_api.unlock()

    def main(self) -> None:
        rdwr_options = {
            "targets": ["212F", "424F"],  # read as Type3 (FeliCa／FeliCa Lite-S) ref.
            # https://www.sony.co.jp/Products/felica/about/scheme.html
            "on-connect": self.on_connect,
        }
        with nfc.ContactlessFrontend("usb") as clf:
            try:
                while True:
                    clf.connect(rdwr=rdwr_options)
                    time.sleep(SLEEP_SEC)
            except IOError as error:
                if error.errno == errno.EIO:
                    logger.exception("lost connection to local device")
                else:
                    logger.exception("io error")
            except nfc.clf.UnsupportedTargetError:
                logger.exception("unspported target")
            except KeyboardInterrupt:
                logger.warning("Interrupt by keyboard input")
            finally:
                clf.close()


if __name__ == "__main__":
    reader = SesameNFCReader()
    reader.main()