from django.shortcuts import render, redirect
from django.views import View
from referral.froms import ReferrerAssignmentFrom
from account.models import User
from referral.models import ReferralReferrer
from django.contrib import messages


class ProfileView(View):
    """
    User profile in the referral program.
    """

    form_class = ReferrerAssignmentFrom
    template_name = "referral/profile_in_referral_program.html"
    page_title = "Referral Program"

    def get(self, request):
        variables = {"page_title": self.page_title}

        variables["invite_code"] = request.user.invite_code

        # If the user has already defined his referrer, 
        #   the previously entered referrer invite code 
        #   will be displayed for the user 
        #   in the corresponding section, 
        #   otherwise the user will be provided with a form 
        #   for specifying his referrer
        referrer_of_authorized_user = \
            ReferralReferrer.objects.select_related("referrer") \
                .filter(pk=request.user).first()
        if referrer_of_authorized_user:
            variables["referrer"] = \
                referrer_of_authorized_user.referrer.invite_code
        else:
            variables["form"] = ReferrerAssignmentFrom()

        # Getting the phone numbers of the current user's referrals 
        #   to display in the user's profile
        variables["phones_owned_by_referrals"] = [
            referral_and_referrer.referral.phone_number
            for referral_and_referrer in ReferralReferrer.objects \
                .select_related("referral") \
                .filter(referrer=request.user)
        ]

        return render(request, self.template_name, variables)

    def post(self, request):
        # Checking the validity of the invite code for the referrer 
        #   entered by the user
        if self.form_class(request.POST).is_valid():
            referrer_invite_code = request.POST["referrer_code"].upper()
            referrer_of_authorized_user = User.objects \
                .filter(invite_code=referrer_invite_code).first()

            # Checking the invite code sent by the user 
            #   in the post request for several criteria: 
            #   whether there is a user in the database 
            #   with the transferred invite code 
            #   and whether the user 
            #   who owns the transferred invite code could invite 
            #   the current user based on the sequence of registration 
            #   of these users in the system
            if referrer_of_authorized_user is not None:
                if referrer_of_authorized_user.id < request.user.id:
                    ReferralReferrer.objects.create(
                        referral=request.user,
                        referrer=referrer_of_authorized_user
                    )
                    return redirect("profile")

        # Messages for the quick message system informing the user 
        #   about the reasons for not accepting 
        #   the invite code entered by the user
                else:
                    message = "Your referrer must be registered before you"
            else:
                message = "The user with the specified invite code " \
                "does not exist"
        else:
            message = "The invite code must be six characters long " \
                "and contain only numbers and latin letters."

        messages.add_message(
            request,
            messages.INFO,
            message
        )

        return redirect("profile")