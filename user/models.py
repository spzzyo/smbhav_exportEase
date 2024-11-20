from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.
    """
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    """
    Custom User model extending the AbstractUser.
    Includes a user_type field to distinguish roles.
    """
    USER_TYPE_CHOICES = (
        (1, "Admin"),
        (2, "Exporter"),
        (3, "Shipper"),
    )

    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES,
        default=3,  # Default to "Viewer"
        verbose_name="User Type"
    )

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
