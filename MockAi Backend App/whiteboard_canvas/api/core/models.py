from django.db import models

# Create your models here.
""" Core Model """
import uuid

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator


class BaseModelMixin(models.Model):
    """ Abstract Model to be extended by all other models """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=32)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EmailUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email,
                     password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(
            username=username, email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username,
                    email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password,
                                 **extra_fields)

    def create_superuser(self, username, email, password,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password,
                                 **extra_fields)


class EmailAbstractUser(AbstractUser, BaseModelMixin):
    email = models.EmailField(unique=True,)
    objects = EmailUserManager()

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True


class CanvasUser(EmailAbstractUser):
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    phone_number = models.IntegerField(validators=[MaxValueValidator(9999999999)], null=False)
    address = models.TextField(null=True)
    city = models.TextField(null=True)
    state = models.TextField(null=True)
    country = models.TextField(null=True)
    pincode = models.IntegerField(validators=[MaxValueValidator(999999)], null=False)
    is_admin = models.BooleanField(default=False)


class Conversation(BaseModelMixin):
    applicant = models.ForeignKey(CanvasUser, on_delete=models.CASCADE, related_name="applicant", null=True)
    applicant_request = models.TextField(null=True)
    ai_response = models.TextField(null=True)
    applicant_diagram = models.FileField(upload_to='images/', null=True)
    applicant_audio = models.FileField(upload_to='audio/', null=True)


