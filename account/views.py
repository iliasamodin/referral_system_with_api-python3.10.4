from django.shortcuts import render, redirect
from django.views import View
from account.froms import PhoneValidationForm, AuthorizationForm
from django.conf import settings
from django.contrib import messages
from account.models import User
from django.contrib.auth import login
from random import randint
from time import sleep


class AuthorizationView(View):
    """
    Authorization of users in the referral system via SMS.
    """

    template_name = "account/referral_program_authorization.html"
    page_title = "Authorization"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("profile")

        variables = {"page_title": self.page_title}

        # Using multiple forms for different authorization steps
        if not "validation_passed" in request.session:
            variables["form"] = PhoneValidationForm(
                # Initialization of the phone number input form 
                #   by the user number whose invite code 
                #   has already been accepted as a referrer 
                #   for other users. 
                #   This initialization is used 
                #   only for the demo version of the project 
                #   to clearly show the display 
                #   of referrals in the profile
                initial={"phone_number": 7_999_111_00_00} 
                if settings.DEMO else {}
            )

        else:
            variables["form"] = AuthorizationForm(
                # The authorization_code field 
                #   is initialized only in the demo version
                initial={
                "authorization_code": 
                request.session["validation_passed"]["authorization_code"]
                } if settings.DEMO else {}
            )

        return render(request, self.template_name, variables)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("profile")

        # Phone number validation step
        if not "validation_passed" in request.session:
            # Validation of the number entered by the user
            if PhoneValidationForm(request.POST).is_valid():
                # Storing authentication data in the session 
                request.session["validation_passed"] = dict()
                request.session["validation_passed"]["phone_number"] = \
                    request.POST["phone_number"]
                # Pseudo-random authorization code generation
                request.session["validation_passed"]["authorization_code"] = \
                    str(randint(1000, 9999))

                # Simulation of sending a 4-digit authorization code
                sleep(1)

            else:
                # Adding a flash message for a user 
                #   whose number did not pass validation
                messages.add_message(
                    request, 
                    messages.INFO, 
                    "Enter only the digits of your number,\n"
                    "no spaces or other characters"
                )

        # SMS user authorization stage
        else:
            phone_number = request.session["validation_passed"]["phone_number"]
            authorization_code = \
                request.session["validation_passed"]["authorization_code"]

            # Checking if the code entered by the user in the form matches 
            #   the code that was sent via SMS 
            #   to the number specified by the user
            if AuthorizationForm(request.POST).is_valid() and\
            request.POST["authorization_code"] == authorization_code:
                # Removing data that is no longer needed from the session
                del request.session["validation_passed"]

                user, _ = User.get_or_create(phone_number=phone_number)

                # User authorization
                login(request, user)
                return redirect("profile")

            # If the user entered an incorrect authorization code, 
            #   a corresponding message is displayed for him 
            #   and the authorization process starts over
            else:
                del request.session["validation_passed"]

                messages.add_message(
                    request, 
                    messages.INFO, 
                    "You have entered an invalid access code"
                )

        return redirect("login")
