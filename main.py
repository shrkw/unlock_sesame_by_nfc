import binascii
import errno
import time

import nfc

SLEEP_SEC = 1


class SesameNFCReader:
    def validate_idm(self, idm: str) -> bool:
        print(idm)
        return True

    def on_connect(self, tag: nfc.tag.Tag) -> None:
        print(tag)
        idm = binascii.hexlify(tag.identifier).decode().upper()
        if self.validate_idm(idm):
            # TODO send request to sesame api
            pass

    def main(self) -> None:
        rdwr_options = {
            "targets": ["212F", "424F"],  # read as Type3 (FeliCa／FeliCa Lite-S)
            "on-connect": self.on_connect,
        }
        with nfc.ContactlessFrontend("usb") as clf:
            try:
                while True:
                    clf.connect(rdwr=rdwr_options)
                    time.sleep(SLEEP_SEC)
            except IOError as error:
                if error.errno == errno.EIO:
                    print("lost connection to local device")
                else:
                    print(error)
            except nfc.clf.UnsupportedTargetError as error:
                print(error)
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":
    reader = SesameNFCReader()
    reader.main()
