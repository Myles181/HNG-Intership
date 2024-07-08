from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, firstName, lastName, password=None, phone=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not firstName:
            raise ValueError('Users must have a first name')
        if not lastName:
            raise ValueError('Users must have a last name')
        if not password:
            raise ValueError('Users must have a password')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            firstName=firstName,
            lastName=lastName,
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstName, lastName, password=None, phone=None):
        user = self.create_user(
            email=email,
            firstName=firstName,
            lastName=lastName,
            password=password,
            phone=phone,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    userId = models.CharField(max_length=10, editable=False, unique=True)
    firstName = models.CharField(max_length=30, null=False)
    lastName = models.CharField(max_length=30, null=False)
    email = models.EmailField(unique=True, null=False)
    phone = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

class Organisation(models.Model):
    orgId = models.CharField(max_length=10, editable=False, unique=True)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User, related_name='organisations')

    def __str__(self):
        return self.name
