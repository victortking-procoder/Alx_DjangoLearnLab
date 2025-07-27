from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return self.title

class CustomUserManager(BaseUserManager): # Inherit from BaseUserManager
    """
    Custom user manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Use create_user to ensure consistent handling of common fields
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    # If you want to use email as the primary username field,
    # you might want to make 'email' unique and change USERNAME_FIELD.
    # For now, we'll keep 'username' as the USERNAME_FIELD from AbstractUser,
    # but still emphasize email in the manager.

    # Make email unique if you intend to use it as a primary identifier for login
    email = models.EmailField(_('email address'), unique=True)

    date_of_birth = models.DateField(
        _('date of birth'),
        null=True,
        blank=True
    )
    profile_photo = models.ImageField(
        _('profile photo'),
        upload_to='profile_photos/',
        null=True,
        blank=True
    )

    # Set the custom manager
    objects = CustomUserManager()

    # If you intend to use email for login, uncomment the next line
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username'] # Add any other required fields that are not the USERNAME_FIELD

    class Meta:
        verbose_name = _('custom user')
        verbose_name_plural = _('custom users')

    def __str__(self):
        # Depending on your USERNAME_FIELD, you might return email or username
        return self.username # Or self.email if USERNAME_FIELD is 'email'