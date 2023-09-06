from django.shortcuts import render
from django.views import View


class ProfileView(View):
    """
    User profile in the referral program.
    """

    template_name = "referral/profile_in_referral_program.html"
    page_title = "Referral Program"

    def get(self, request):
        return render(request, self.template_name)