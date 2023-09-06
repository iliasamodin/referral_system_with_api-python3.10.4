from django.contrib import admin
from referral.models import ReferralReferrer


@admin.register(ReferralReferrer)
class ReferralReferrerAdmin(admin.ModelAdmin):
    list_display = ["referral", "referrer"]
    list_filter = ["referrer"]