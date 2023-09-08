from django.shortcuts import render, redirect
from django.views import View
from referral.froms import ReferrerAssignmentFrom
from instruction.models import Key
from account.models import User
from referral.models import ReferralReferrer
from django.contrib import messages

from rest_framework.views import APIView
from referral.serializers import (
    ProfileSerializer, 
    InviteCodeSerializer,
    ReferrerSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ProfileView(View):
    """
    User profile in the referral program.
    """

    form_class = ReferrerAssignmentFrom
    template_name = "referral/profile_in_referral_program.html"
    page_title = "Referral Program"

    def get(self, request):
        variables = {"page_title": self.page_title}

        if request.GET.get("section") == "Instruction":
            variables["instructions"] = \
                Key.objects.select_related("api_path").all()

        else:
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


class ProfileAPIView(APIView):
    """
    API for user profile.
    """

    queryset = ReferralReferrer.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = self.queryset \
            .select_related("referrer") \
            .filter(referrer=request.user)

        # Returning a list type response
        return Response(
            self.serializer_class(instance=queryset, many=True).data
        )


class InviteCodeAPIView(APIView):
    """
    API for receiving an invite code 
    authorized in the referral program of the user.
    """

    serializer_class = InviteCodeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(self.serializer_class(instance=request.user).data)


class ReferrerAPIView(APIView):
    """
    API for obtaining and assignment the referrer.
    """

    queryset = ReferralReferrer.objects.all()
    serializer_class = ReferrerSerializer
    permission_classes = [IsAuthenticated]

    def get_referrer(self, request):
        queryset = self.queryset \
            .select_related("referrer") \
            .filter(pk=request.user).first()
        referrer_of_authorized_user = \
            self.serializer_class(instance=queryset).data
        return referrer_of_authorized_user

    def get(self, request):
        referrer_of_authorized_user = self.get_referrer(request)

        # If the user has not yet indicated 
        #   the invite code of his referrer, 
        #   the corresponding message is returned to the user
        if not referrer_of_authorized_user["referrer_code"]:
            response_messages = {
                "message": 
                "Pass your referrer invite code by 'referrer_code' key"
            }
            return Response(response_messages)

        return Response(referrer_of_authorized_user)

    def post(self, request):
        referrer_of_authorized_user = self.get_referrer(request)

        # If the referrer for the user is already defined, 
        #   then when trying to redefine the referer, 
        #   the user will return the invite code 
        #   of the previously defined referrer 
        #   and an informational message about 
        #   the impossibility of redefining the referer
        if referrer_of_authorized_user["referrer_code"]:
            referrer_of_authorized_user["message"] = \
                "Referrer previously defined and cannot be changed"

            return Response(referrer_of_authorized_user)

        else:
            if self.serializer_class(data=request.data).is_valid():
                referrer_invite_code = request.data["referrer_code"].upper()
                referrer_of_authorized_user = User.objects \
                    .filter(invite_code=referrer_invite_code).first()

                if referrer_of_authorized_user is not None:
                    if referrer_of_authorized_user.id < request.user.id:
                        ReferralReferrer.objects.create(
                            referral=request.user,
                            referrer=referrer_of_authorized_user
                        )
                        return redirect("referrer_api")

                    else:
                        message = "Your referrer must be registered before you"
                else:
                    message = "The user with the specified invite code " \
                    "does not exist"
            else:
                message = "Pass a six-digit invite code for the 'referrer' key"

            response_messages = {"message": message}
            return Response(response_messages)
