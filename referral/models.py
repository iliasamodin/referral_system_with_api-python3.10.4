from django.db import models
from account.models import User


# One-to-many relationship model for referrers and referrals
class ReferralReferrer(models.Model):
    referral = models.OneToOneField(
        User, 
        null=False,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="user_referral"
    )
    referrer = models.ForeignKey(
        User, 
        null=False, 
        on_delete=models.CASCADE,
        related_name="user_referrer"
    )

    class Meta:
        ordering = ["referrer", "referral"]

    def __str__(self):
        return f"{self.referrer} invited {self.referral}"