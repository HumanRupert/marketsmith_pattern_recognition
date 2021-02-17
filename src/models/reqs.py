from pydantic import BaseModel


class LoginPayload(BaseModel):
    include = "profile,data,"
    includeUserInfo = "true"
    loginID: str
    password: str
    ApiKey: str
