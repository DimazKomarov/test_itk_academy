from repositories.base import BaseRepository
from core.models.users import User


class UserRepository(BaseRepository):
    model = User
