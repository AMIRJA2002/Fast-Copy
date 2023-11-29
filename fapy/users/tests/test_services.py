from ..data_transfer.repository import UserRepository, LoginOTPRepository
from ..services import LoginUser, ValidateLogin, generate_login_otp
from ..data_transfer.filter_builder import UserFilterBuilder
from django.contrib.auth import get_user_model
from django.core.exceptions import BadRequest
from django.http import Http404
from django.test import TestCase

User = get_user_model()


class RegisterUserTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        repository = UserRepository()
        data = {'phone_number': '09190257536', 'password': '123456'}
        cls.user = repository.create(data=data)

    def test_create_user(self):
        self.assertEquals(self.user.phone_number, '09190257536')
        self.assertNotEquals(self.user.password, '123456')


class LoginUserTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        repository = UserRepository()
        data = {'phone_number': '09190257536', 'password': '123456'}
        repository.create(data=data)
        dict_filter = {'phone_number': '09190257536'}
        cls.user = repository.get(dict_filter)

    def test_check_phone_number(self):
        self.assertEquals(self.user.phone_number, '09190257536')


class OtpLoginTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.repository = LoginOTPRepository
        cls.otp = '987654'
        cls.phone_number = '09190257536'
        cls.service = LoginUser(repository=UserRepository, dict_filter={'phone_number': '09190257536'})

    def test_check_phone_number_with_saved_otp_in_redis(self):
        self.repository().save(phone_number=self.phone_number, otp=self.otp, expired=120)

        with self.assertRaises(BadRequest):
            self.service.store_otp_in_cache(repository=self.repository, otp=self.otp)

    def test_check_phone_number_without_saved_otp_in_redis(self):
        self.repository().save(phone_number=self.phone_number, otp=self.otp, expired=120)
        otp_in_redis = self.repository().get(phone_number=self.phone_number)
        self.assertEquals(self.otp, otp_in_redis)


class ValidateLoginTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.repository = LoginOTPRepository
        cls.phone_number = '09190257536'
        cls.otp = '987654'
        cls.service = ValidateLogin

    def test_check_otp_with_wrong_otp(self):
        service = self.service(repository=self.repository, phone_number=self.phone_number, otp='12365')
        with self.assertRaises(BadRequest):
            service.check_otp()

    def test_check_otp_with_right_otp(self):
        service = self.service(repository=self.repository, phone_number=self.phone_number, otp=self.otp)
        self.assertEquals(service.check_otp(), None)

    def test_delete_used_keys_with_right_data(self):
        repository = self.repository()
        repository.save(phone_number=self.phone_number, otp=self.otp)
        service = self.service(repository=LoginOTPRepository, phone_number=self.phone_number, otp=self.otp)
        service.delete_used_keys()
        self.assertEquals(repository.get(phone_number=self.phone_number), None)

    def test_get_user_object_with_wrong_data(self):
        with self.assertRaises(Http404):
            self.service.get_user_object(repository=UserRepository, dict_filter={'phone_number': '123'})

    def test_get_user_object_with_right_data(self):
        dict_filter = UserFilterBuilder(phone_number=self.phone_number)
        UserRepository().create({'phone_number': self.phone_number, 'password': '123456'})
        user = self.service.get_user_object(repository=UserRepository, dict_filter=dict_filter.get_dict_filter())

        self.assertEquals(user.phone_number, self.phone_number)
        self.assertNotEquals('091902', self.phone_number)
        self.assertNotEquals(user.password, '123456')


class GenerateOPTTestCase(TestCase):

    def test_generate_login_otp(self):
        otp = generate_login_otp()
        self.assertEqual(len(otp), 6)
        self.assertEquals(type(otp), str)
