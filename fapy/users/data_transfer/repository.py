from ...common.base_repository import BaseRepository as BR
from ...common.redis_connection import RedisConnection
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRepository(BR):
    def __init__(self, model: User = User) -> None:
        self.model = model
        super(UserRepository, self).__init__(self.model)

    def create(self, data):
        return self.model.objects.create_user(**data)


class LoginOTPRepository(RedisConnection):

    def save(self, phone_number: str, otp: str, expired: int = None) -> None:
        conn = self.connection()
        if not expired:
            conn.set(phone_number, otp)
        else:
            conn.set(phone_number, otp, ex=expired)

    def get(self, phone_number: str) -> str:
        conn = self.connection()
        return conn.get(phone_number)

    def delete(self, phone_number: str) -> None:
        conn = self.connection()
        conn.delete(phone_number)
