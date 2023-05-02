import requests
from typing import Optional


class UnimiSessionManager:
    """Manages Ariel's login session as singleton"""

    session: Optional[requests.Session] = None

    @staticmethod
    def getSession(email: str = "", password: str = ""):
        """
        Returns the session.
        The first time it needs `email` and `password`, subsequent calls
        won't need them.
        Raises `requests.HTTPError` if at the first call `email` or `password`
        are wrong.
        """
        if UnimiSessionManager.session is None:
            UnimiSessionManager.session = requests.Session()
            login_url = "https://elearning.unimi.it/authentication/skin/portaleariel/login.aspx?url=https://ariel.unimi.it/"
            payload = {"hdnSilent": "true",
                       "tbLogin": email, "tbPassword": password}
            response = UnimiSessionManager.session.post(
                url=login_url, data=payload)
            response.raise_for_status()
        return UnimiSessionManager.session
