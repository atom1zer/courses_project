from core.utils.models import (
    AbstractModel,
    AbstractManager,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.db import models


class UserManager(AbstractManager, BaseUserManager):
    def create_user(self, email, name=None, password=None, **kwargs):
        """Create and return a user with an email and password."""
        email = self.normalize_email(email)
        name = email.split('@')[0] if name == None else name
        user = self.model(email=email, name=name, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, password=None, **kwargs):
        """Create and return a superuser with an email and password."""
        kwargs.setdefault("is_admin", True)
        return self.create_user(email, password, **kwargs)


class User(AbstractModel, AbstractBaseUser):

    email = models.EmailField(
        unique=True,
        max_length=50,
        verbose_name="Email",
    )
    name = models.CharField(
        max_length=20,
        verbose_name="Name",
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name="Active",
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name="Superadmin",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
