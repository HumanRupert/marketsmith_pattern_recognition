from pydantic import BaseModel


class User(BaseModel):
    """Represents a MarketSmith `User` object"""
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
