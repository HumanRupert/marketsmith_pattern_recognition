import os
import json

from requests import Session
from dotenv import load_dotenv

from src.ms.endpoints import HANDLE_LOGIN, GET_LOGIN
from src.models import LoginPayload

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

        username = os.environ["USERNAME"]
        password = os.environ["PASSWORD"]
        api_key = os.environ["API_KEY"]
        payload = LoginPayload(
            loginID=username, password=password, ApiKey=api_key)

        # make auth payload accessible to class consumers
        self.payload = payload

        # make a request to GET_LOGIN endpoint to get login info
        login = session.post(GET_LOGIN, data=payload.__dict__).json()
        login["action"] = "login"
        login_json = json.dumps(login)

        # pass the login info to HANDLE_LOGIN endpoint to get .ASPXAUTH cookies
        session.post(HANDLE_LOGIN, data=login_json)

        session.headers.update({'Content-Type': 'application/json'})

        self.session = session
