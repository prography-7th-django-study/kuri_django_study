from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, first_name, password, **other_fields)

    def create_user(self, email, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

### A string describing the name of the field on the user model that is used as the unique identifier.
    # This will usually be a username of some kind, but it can also be an email address, or any other unique identifier.
    # The field must be unique (i.e., have unique=True set in its definition),
    # unless you use a custom authentication backend that can support non-unique usernames.
    USERNAME_FIELD = 'email'
    objects = CustomAccountManager()

### A list of the field names that will be prompted for when creating a user via the createsuperuser management command.
    # The user will be prompted to supply a value for each of these fields.
    # It must include any field for which blank is False or undefined and may include additional fields
    # you want prompted for when a user is created interactively.
    # REQUIRED_FIELDS has no effect in other parts of Django, like creating a user in the admin.
    REQUIRED_FIELDS = ['first_name']
