from pydantic import validate_arguments

from src.ms.auth import AuthSession
from src.ms.endpoints import GET_USER_INFO
from src.models import User


@validate_arguments(config=dict(arbitrary_types_allowed=True))
def get_user(session: AuthSession):
    response = session.session.get(GET_USER_INFO)
    user = User(**response.json())
    return user
