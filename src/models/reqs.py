from pydantic import BaseModel


class LoginPayload(BaseModel):
    """Payload passed to https://login.investors.com/accounts.login to get login info"""
    include = "profile,data,"
    includeUserInfo = "true"
    loginID: str
    password: str
    ApiKey: str
