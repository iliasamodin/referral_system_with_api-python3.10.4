from django.shortcuts import render, redirect
from django.views import View
from account.froms import PhoneValidationForm, AuthorizationForm
from django.conf import settings
from django.contrib import messages
from instruction.models import Key
from account.models import User
from django.contrib.auth import login, logout
from random import randint
from time import sleep

from rest_framework.views import APIView
from account.serializers import (
    ValidationSerializer, 
    AuthorizationSerializer,
    LoginSerializer
)
from account.permissions import IsUnauthorized
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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

        # Depending on the section activated by the user, 
        #   the user will be shown either an authorization page or 
        #   instructions for using the site api
        if request.GET.get("section") == "Instruction":
            variables["instructions"] = \
                Key.objects.select_related("api_path").all()

        else:
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


class LogoutView(View):
    """
    Logout of a user account.
    """

    def get(self, request):
        return redirect("profile")

    def post(self, request):
        logout(request)
        return redirect("login")


class AuthorizationAPIView(APIView):
    """
    API for phone number validation and authorization code generation.
    """

    # Using multiple serializers 
    #   for post requests at different stages of authorization
    serializer_classes = {
        "validation": ValidationSerializer,
        "authorization": AuthorizationSerializer,
        "login": LoginSerializer
    }
    # Restriction on working with the view: only for unauthorized users
    permission_classes = [IsUnauthorized]

    # A property that returns the serializer 
    #   required at the current authorization stage
    @property
    def serializer_class(self):
        if "authorization_passed" in self.request.session:
            return self.serializer_classes["login"]
        elif "validation_passed" in self.request.session:
            return self.serializer_classes["authorization"]
        else:
            return self.serializer_classes["validation"]

    def get(self, request):
        if not "validation_passed" in request.session:
            # Hint at the phone number validation stage
            response_messages = {
                "message": 
                "Pass your phone number by 'phone_number' key"
            }
            return Response(response_messages)

        else:
            response_messages = {
                "message": 
                "Pass code from SMS by 'authorization_code' key"
            }
            if settings.DEMO:
                response_messages["code"] = \
                    request.session['validation_passed']['authorization_code']
            return Response(response_messages)

    def post(self, request):
        if not "validation_passed" in request.session:
            if self.serializer_class(data=request.data).is_valid():
                request.session["validation_passed"] = dict()
                request.session["validation_passed"]["phone_number"] = \
                    str(request.data["phone_number"])
                authorization_code = str(randint(1000, 9999))
                request.session["validation_passed"]["authorization_code"] = \
                    authorization_code

                sleep(1)

        else:
            phone_number = request.session["validation_passed"]["phone_number"]
            authorization_code = \
                request.session["validation_passed"]["authorization_code"]

            if self.serializer_class(data=request.data).is_valid() and \
            str(request.data["authorization_code"]) == authorization_code:
                del request.session["validation_passed"]

                user, _ = User.get_or_create(phone_number=phone_number)

                login(request, user)

                # Returning authorized user data
                request.session["authorization_passed"] = True
                # Installing a serializer by a model object
                authorized_user_data = \
                    self.serializer_class(instance=user).data
                del request.session["authorization_passed"]

                return Response(authorized_user_data)

            else:
                del request.session["validation_passed"]

        # Redirecting the user from the phone number validation stage 
        #   to the SMS authorization stage, 
        #   or from the SMS authorization stage back 
        #   to the phone number validation stage 
        #   if the user entered an incorrect authorization code
        return redirect("login_api")


class LogoutAPIView(APIView):
    """
    API for logout.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        response_messages = {"message": "You are logged out"}
        return Response(response_messages)
