import argparse
import binascii
import errno
import logging
import time

import nfc

import permission_checker
import sesame_api

SLEEP_SEC = 1


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class SesameNFCReader:
    def __init__(self, dryrun: bool = True):
        self.permission_checker = permission_checker.PermissionChecker()
        self.dry_run = dryrun

    def on_connect(self, tag: nfc.tag.Tag) -> None:
        logger.info(tag)
        idm = binascii.hexlify(tag.identifier).decode().upper()
        if self.permission_checker.validate_idm(idm):
            if not self.dry_run:
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
    parser = argparse.ArgumentParser(description="Unlock SESAME lock by NFC")
    parser.add_argument("--dryrun", action="store_true")
    args = parser.parse_args()
    reader = SesameNFCReader(args.dryrun)
    reader.main()
