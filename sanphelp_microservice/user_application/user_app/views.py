import boto3
import uuid

from django.conf import settings

from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from user_app import helper, error_conf
from user_app import system_error
from user_app.models import User
from user_app.serializers import (
    UserSerializer,
)


class CreateUserView(CreateAPIView):
    """
    Creating API for User creation which takes user
    details(email, password, confirm_password, first_name
    last_name, phone_number) as input validates the user details and
    creates a user account.
    """
    model = User
    serializer_class = UserSerializer

    def post(self, request):
       
        user_data         = request.data
        client            = boto3.client('cognito-idp')
        user_data['role'] = "Normal User"
        client_id         = settings.CLIENT_ID
       
        error_checks = system_error.check_for_registration_input_error(
            user_data)

        if error_checks:
            return Response(error_checks,
                            status=status.HTTP_412_PRECONDITION_FAILED)

        try:
            aws_user = client.sign_up(
                ClientId = client_id,
                Username = user_data['email'],
                Password = user_data['password'],
                )
        except Exception:
            return Response(error_conf.GENERIC_API_FALIURE, 
                                status = status.HTTP_400_BAD_REQUEST)

        user_data['id'] = uuid.UUID(aws_user['UserSub'])
        serializer = UserSerializer(data = user_data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'success': True,
                'msg': 'Registration Successfully Please Verify Email'})

        return Response(error_conf.GENERIC_API_FALIURE,
                        status = status.HTTP_412_PRECONDITION_FAILED)


class ConfirmSignup(APIView):
    """
    An API for confirm user sign-up
    """
    def post(self, request, format=None):
    
        if request.data:
            user_data = request.data
            client_id = settings.CLIENT_ID   
            client    = boto3.client('cognito-idp')

            try:
                response = client.confirm_sign_up(
                    ClientId = client_id,
                    Username = user_data['username'],
                    ConfirmationCode = user_data['code'],
                    ForceAliasCreation = True
                )
            except:
                return Response({
                    'msg': 'Verification code does not match'})

            return Response({
                    'success': True,
                    'msg': 'Email Verified'})

        return Response(error_conf.NO_INPUT_DATA,
                        status = status.HTTP_412_PRECONDITION_FAILED)


class UserUpdatePassword(APIView):
    """
    API Used For Updating User Password:
    @i/p user_id, current password, new_password
    @o/p success or failure messgaes
    """

    def post(self, request, format=None):

        data         = request.data
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        access_token = data.get('access_token')
        
        error_checks = system_error.check_for_update_password_input_error(request)
        if error_checks:
            return Response(error_checks,
                            status = status.HTTP_412_PRECONDITION_FAILED)

        client = boto3.client('cognito-idp')    
        response = client.change_password(
                    PreviousPassword = old_password,
                    ProposedPassword = new_password,
                    AccessToken = access_token
                )            

        user_obj = User.objects.filter(id = uuid.UUID(
            data.get('user_id')))

        if user_obj:
            user_obj[0].set_password(new_password)
            user_obj[0].save()

        return Response({
            'success': True,
            'msg': 'Password Updated Successfully',
            })


class LoginView(APIView):
    """
    Creating API for User Authentication
    Based On roles and UserName and Passwords

    Note:-
    Checks whether the request is from audetemi user
    by checking the provider name in UserSocialDetails
    Table and if that entry is primary.
    """

    def post(self, request, format=None):
        """
        Return a Valid token if username and password
        is valid for a given client
        """
        if request.data:

            data = request.data

            error_checks = system_error.check_for_login_input_error(data)

            if (error_checks and error_checks.get('error_code') != 7):
                return Response(error_checks,
                                status = status.HTTP_412_PRECONDITION_FAILED)

            email     = data.get('email')
            password  = data.get('password')
            source    = data.get('source')
            user      = User.objects.get(email = email)
            username  = user.username
            client_id = settings.CLIENT_ID
            client    = boto3.client('cognito-idp')
            
            try:
                response = client.admin_initiate_auth(
                    UserPoolId = 'us-east-2_uv2An2oJh',
                    ClientId = client_id,
                    AuthFlow='ADMIN_NO_SRP_AUTH',
                    AuthParameters = {
                    'USERNAME': user.email,
                    'PASSWORD':password,
                })

            except Exception:
                return Response(error_conf.GENERIC_API_FALIURE,
                                status = status.HTTP_412_PRECONDITION_FAILED)

            if (user.role == User.UserTypes.NORMAL_USER.value
                    and source == 'USER_APP' 
                    or user.role == User.UserTypes.AGENT.value
                    and source == 'AGENT_APP' or user.is_superuser):

                return Response({
                    'success': True,
                    'msg': 'Logged in Successfully.',
                    'response':response})

        return Response(error_conf.NO_INPUT_DATA,
                        status = status.HTTP_412_PRECONDITION_FAILED)


class UserLogout(APIView):
    """
    Creating API for sign out from application
    This is global sign out, It will sign out from all microservices

    Note - Check whether the access token passed in request for logout
    """

    def post(self, request, format=None):
        if request.data:
            data         = request.data
            access_token = data.get('accesstoken')
            client       = boto3.client('cognito-idp')

            try:
                response = client.global_sign_out(
                    AccessToken = access_token
                    )
            except:
                return Response({
                    'msg':'Access token does not match'
                    })

            return Response({
                'success': True,
                'msg': 'Logged out Successfully',
                'response':response})

        return Response(error_conf.NO_INPUT_DATA,
                status = status.HTTP_412_PRECONDITION_FAILED)
