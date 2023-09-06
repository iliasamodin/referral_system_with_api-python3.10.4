from rest_framework import serializers
from account.models import User


class ValidationSerializer(serializers.Serializer):
    """
    Serializer for validating the phone number passed by the user.
    """

    phone_number = serializers.IntegerField(
        min_value=1_000_000_000,
        max_value=999_999_999_999_999,
        write_only=True  
    )


class AuthorizationSerializer(serializers.Serializer):
    """
    Serializer for validating the authorization code 
    passed by the user.
    """

    authorization_code = serializers.IntegerField(
        min_value=1_000,
        max_value=9_999,
        write_only=True
    )


class LoginSerializer(serializers.ModelSerializer):
    """
    Serializer for returning data about the logged in user.
    """

    class Meta:
        model = User
        fields = ["phone_number", "invite_code", "is_superuser", "is_staff"]
        extra_kwargs = {
            "phone_number": {"read_only": True},
            "invite_code": {"read_only": True},
            "is_superuser": {"read_only": True},
            "is_staff": {"read_only": True}
        }