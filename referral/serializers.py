from rest_framework import serializers
from referral.models import ReferralReferrer
from account.models import User


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for returning phone numbers belonging to referrals.
    """

    phone_number = serializers.CharField(
        source="referral.phone_number",
        read_only=True
    )

    class Meta:
        model = ReferralReferrer
        fields = ["phone_number"]
        depth = 1


class InviteCodeSerializer(serializers.ModelSerializer):
    """
    Serializer to return the user's invite code.
    """

    class Meta:
        model = User
        fields = ["invite_code"]
        extra_kwargs = {
            "invite_code": {"read_only": True}
        }


class ReferrerSerializer(serializers.ModelSerializer):
    """
    Serializer for validation and return of referrer invite code.
    """

    referrer_code = serializers.CharField(
        source="referrer.invite_code",
        min_length=6,
        max_length=6
    )

    class Meta:
        model = ReferralReferrer
        fields = ["referrer_code"]
        depth = 1
