from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone


class PPIUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email address must be set')

        now = timezone.now()
        email = PPIUserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        superuser = self.create_user(email, password, **extra_fields)
        superuser.is_staff = True
        superuser.is_active = True
        superuser.is_superuser = True
        superuser.save(using=self._db)
        return superuser


class PPIUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False,
        editable=True,
    )
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(
        default=timezone.now,
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'

    objects = PPIUserManager()

    # There is no firstname and lastname in PPIUser this function returns email
    def get_full_name(self):
        return self.email

    # There is no first name in PPIUser this function returns email.
    def get_short_name(self):
        return self.email
