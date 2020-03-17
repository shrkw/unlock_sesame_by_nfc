import csv
import logging

logger = logging.getLogger(__name__)


class PermissionChecker:
    def __init__(self):
        with open("permissions.csv", "r") as f:
            reader = csv.DictReader(f)
            self.permissions = {row["idm"]: row["name"] for row in reader}

    def validate_idm(self, idm: str) -> bool:
        if idm not in self.permissions:
            logger.warning(f"Not Permitted: {idm}")
            return False
        logger.info(f"Permitted: {idm}, for User: {self.permissions[idm]}")
        return True
