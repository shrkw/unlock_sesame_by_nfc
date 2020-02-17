import json
import logging

logger = logging.getLogger(__name__)


class PermissionChecker:
    def __init__(self):
        with open("permissions.json", "r") as f:
            self.permissions = json.load(f)

    def validate_idm(self, idm: str) -> bool:
        if idm not in self.permissions:
            logger.warning(f"Not Permitted: {idm}")
            return False
        logger.info(f"Permitted: {idm}, for User: {self.permissions[idm]['name']}")
        return True
