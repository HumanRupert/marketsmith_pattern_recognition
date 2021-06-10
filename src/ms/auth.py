import os
import json

from requests import Session
from dotenv import load_dotenv

from src.ms.endpoints import HANDLE_LOGIN, GET_LOGIN

load_dotenv()


class AuthSession:
    def __init__(self):
        """Generates a session authenticated into MarketSmith

        Notes
        -------
        Uses the following environment variables for authentication:
        - USERNAME
        - PASSWORD
        - API_KEY

        Returns
        -------
        Session
            An authenticated requests session.

        """
        session = Session()

        payload = {
            "loginID": os.environ["USERNAME"],
            "password": os.environ["PASSWORD"],
            "ApiKey": os.environ["API_KEY"],
            "include": "profile,data,",
            "includeUserInfo": "true"
        }

        # make auth payload accessible to class consumers
        self.payload = payload

        # make a request to GET_LOGIN endpoint to get login info
        login = session.post(GET_LOGIN, data=payload).json()
        login["action"] = "login"

        # pass the login info to HANDLE_LOGIN endpoint to get .ASPXAUTH cookies
        res = session.post(HANDLE_LOGIN, json=login)

        self.session = session
