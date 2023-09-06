from django.contrib.auth.base_user import BaseUserManager
from account.functions import convert_to_another_system
from random import randint


class UserManager(BaseUserManager):
    """
    Custom user manager based on BaseUserManager 
    designed to change the attributes required to register new users.
    """

    use_in_migrations = True

    def _create_user(
        self, 
        phone_number, 
        invite_code,
        password, 
        **extra_fields
    ):

        """
        Creates and saves a User 
        with the given phone_number, invite_code and password.
        """

        if not phone_number:
            raise ValueError('The given phone_number must be set')
        user = self.model(
            phone_number=phone_number,
            invite_code=invite_code,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, 
        phone_number, 
        invite_code,
        password="", 
        **extra_fields
    ):

        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            phone_number, 
            invite_code,
            password, 
            **extra_fields
        )

    def create_superuser(
        self, 
        phone_number, 
        password, 
        **extra_fields
    ):

        # Random selection of an invite code for a superuser 
        #   among the options starting with ZZ0000
        invite_code = convert_to_another_system(
            randint(2_175_102_720, 2_176_782_335),
            number_system=36
        )

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            phone_number, 
            invite_code,
            password, 
            **extra_fields
        )