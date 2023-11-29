from django.core.exceptions import BadRequest
from django.contrib.auth.models import User
from typing import Dict
import random


class RegisterUser:
    def __init__(self, repository) -> None:
        self.repository = repository()

    def create_user(self, data):
        return self.repository.create(data=data)


class LoginUser:
    def __init__(self, repository, dict_filter: [str, any]) -> None:
        self.repository = repository()
        self.dict_filter = dict_filter

    def check_phone_number(self) -> None:
        self.repository.get(self.dict_filter)

    def store_otp_in_cache(self, repository, otp: str) -> None:
        phone_number = self.dict_filter.get('phone_number', None)
        login_repository = repository()

        if login_repository.get(phone_number=phone_number):
            raise BadRequest('last code is not expired yet')

        login_repository.save(phone_number=phone_number, otp=otp, expired=120)


class ValidateLogin:
    def __init__(self, repository, phone_number: str, otp: str) -> None:
        self.repository = repository()
        self.phone_number = phone_number
        self.otp = otp

        if self.phone_number is None:
            raise BadRequest('phone number is required')

    def check_otp(self) -> None:
        code = self.repository.get(phone_number=self.phone_number)
        if code != self.otp:
            raise BadRequest('code is not valid or expired')

    def delete_used_keys(self) -> None:
        self.repository.delete(phone_number=self.phone_number)

    @staticmethod
    def get_user_object(repository, dict_filter: Dict[str, any]) -> User:
        repository = repository()
        return repository.get(dict_filter=dict_filter)


def generate_login_otp() -> str:
    return str(random.randint(100000, 999999))
