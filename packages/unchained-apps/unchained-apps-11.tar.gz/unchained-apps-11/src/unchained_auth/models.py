import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from unchained_utils.v0.base_classes import LowerCaseEmailField


class UserManager(BaseUserManager):
    def create_user(self, id, email,  password=None):
        if not email:
            raise TypeError('Users must have an email address.')

        user = self.model(id=id, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, id, email, password):
        if not password:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(id, email, password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    objects = UserManager()
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True)
    email = LowerCaseEmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_active = models.BooleanField(null=True)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email']

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.id
