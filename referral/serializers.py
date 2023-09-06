from rest_framework import serializers
from referral.models import ReferralReferrer


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