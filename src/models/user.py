from pydantic import BaseModel


class User(BaseModel):
    CSUserID: int
    DisplayName: str
    EmailAddress: str
    IsSpecialAccount: bool
    RemainingTrialDays: int
    SessionID: str
    UserDataInitializationFailed: bool
    UserEntitlements: str
    UserID: int
    UserType: int
