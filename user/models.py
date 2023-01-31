from django.db import models
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, password, first_name='', last_name='', **kwargs):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        first_name = ''
        last_name = ''
        username = email
        user = self.create_user(email, username, password,
                                first_name, last_name, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    objects = UserManager()

    GENDER_CHOICES = [
        ('M', 'male'),
        ('F', 'female'),
    ]

    email = models.EmailField(("email address"), unique=True)
    gender = models.CharField(choices=GENDER_CHOICES,
                              default='M', max_length=1)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ()

    @ property
    def name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def get_token(self):
        refresh_token = RefreshToken.for_user(self)
        token = refresh_token.access_token
        return str(token)
