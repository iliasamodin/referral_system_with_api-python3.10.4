from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
# Import custom user manager
from account.manager import UserManager
from account.functions import convert_to_another_system


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model based on AbstractBaseUser and PermissionsMixin, 
    designed to personalize user attributes (columns) in the database.
    """

    phone_number = models.CharField(
        _("phone number"), 
        max_length=15, 
        unique=True
    )
    invite_code = models.CharField(
        _("own invite code"), 
        max_length=6, 
        unique=True
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        )
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        )
    )

    # Using a custom manager
    objects = UserManager()

    # A unique field identifying a user in the system
    USERNAME_FIELD = "phone_number"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["invite_code"]

    def get_full_name(self):
        return self.__str__()

    def get_short_name(self):
        return self.__str__()

    def __str__(self):
        return f"{self.phone_number} ({self.invite_code})"

    # 
    @classmethod
    def get_or_create(cls, **kwargs):
        """
        Model class method to get the user from the database 
        if the user exists 
        or create a new user in the database 
        if the user is unregistered.

        The get_or_create method for the User model differs 
        from the get_or_create method from the UserManager 
        by modifying the functionality for creating a new user, 
        taking into account the mandatory presence 
        of the invite_code attribute for each user.
        """

        user = cls.objects.filter(**kwargs).first()
        object_created = False

        # Invite code generation 
        #   and registration of an unregistered user
        if user is None:
            last_user = cls.objects \
                .filter(invite_code__lte="ZXZZZZ").order_by("id") \
                .last()
            if last_user is not None:
                last_invite_code = int(last_user.invite_code, 36)
            else:
                last_invite_code = 0

            invite_code = convert_to_another_system(
                last_invite_code + 1,
                number_system=36
            )
            invite_code = invite_code.rjust(6, "0")

            user = User.objects.create_user(
                invite_code=invite_code,
                **kwargs
            )

            object_created = True

        return user, object_created