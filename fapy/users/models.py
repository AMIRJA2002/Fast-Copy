from django.db import models
from ..common.models import BaseModel
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM


class BaseUserManager(BUM):
    def create_user(self, phone_number, is_active=True, is_admin=False, password=None):
        if not phone_number:
            raise ValueError("Users must have an phone number")

        user = self.model(phone_number=phone_number, is_active=is_active, is_admin=is_admin)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        # user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(
            phone_number=phone_number,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):

    phone_number = models.CharField(verbose_name="phone_number", unique=True, db_index=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return self.phone_number

    def is_staff(self):
        return self.is_admin
