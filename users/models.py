import phonenumbers

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, phonenumber, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not phonenumber:
            raise ValueError(_('Должен быть указан номер телефона'))
        try:
            parsed_phone_number = phonenumbers.parse(
                phonenumber,
                'RU'
            )
        except phonenumbers.NumberParseException:
            raise ValueError(_('Некорректный номер телефона'))
        if not phonenumbers.is_valid_number(parsed_phone_number):
            raise ValueError(_('Некорректный номер телефона'))
        normalized_phone_number = phonenumbers.format_number(
            parsed_phone_number,
            phonenumbers.PhoneNumberFormat.E164
        )
        user = self.model(phonenumber=normalized_phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phonenumber, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(phonenumber, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    phonenumber = PhoneNumberField(_('phone number'), unique=True)

    USERNAME_FIELD = 'phonenumber'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phonenumber