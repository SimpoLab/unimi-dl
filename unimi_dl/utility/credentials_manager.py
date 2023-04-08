import logging

from pathlib import Path
from json import dumps as json_dumps, load as json_load
from typing import Optional

main_logger = logging.getLogger(__name__)


class Credentials:
    def __init__(self, email: Optional[str], password: Optional[str]) -> None:
        self.email = email
        self.password = password


class CredentialsManager:
    """
    Manages the `credentials` configuration file
    """

    def __init__(self, cred_path: str) -> None:
        self.path = Path(cred_path).expanduser()
        with self.path.open("r") as credentials_file:
            credentials_dict = json_load(credentials_file)
            self.credentials = Credentials(
                credentials_dict["email"], credentials_dict["password"]
            )

    def setCredentials(self, email: str, password: str):
        """
        Saves new email and password
        """
        credentials = Credentials(email, password)
        self.credentials = credentials
        credentials.password = password

        with self.path.open("w") as credentials_file:
            credentials_file.write(json_dumps(self.credentials))
            main_logger.info(
                f"Credentials saved succesfully in {str(self.path)}")

    def getCredentials(self) -> Credentials:
        return self.credentials

    def wipeCredentials(self):
        """
        Removes the credentials in `self.path` and sets `self.credentials` properties to None
        """
        from os import remove

        remove(str(self.path))
        self.credentials = Credentials(None, None)
