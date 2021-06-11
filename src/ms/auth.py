import os
import json

from requests import Session
from dotenv import load_dotenv

from src.ms.endpoints import HANDLE_LOGIN, GET_LOGIN

load_dotenv()


class AuthSession:
    def __init__(self,
                 username: str = os.environ["USERNAME"],
                 password: str = os.environ["PASSWORD"],
                 api_key: str = os.environ["API_KEY"],
                 include: str = "profile,data,"
                 ):
        """Generates a session authenticated into MarketSmith"""
        session = Session()

        payload = {
            "loginID": username,
            "password": password,
            "ApiKey": api_key,
            "include": include,
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
