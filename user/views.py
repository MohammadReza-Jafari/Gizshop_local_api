import uuid
import random

from rest_framework import generics, authentication, permissions, status, viewsets, filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.decorators import APIView

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from . import serializers
from core import helpers
from core import permissions as custom_permissions


class SignupView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class GetAuthTokenView(ObtainAuthToken):
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data, context={'request': request})

        if ser.is_valid(raise_exception=True):
            user = ser.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token': token.key,
                    'username': user.name,
                    'email': user.email,
                    'isAdmin': user.is_superuser
                },
                status=status.HTTP_200_OK
            )
        return Response(data=ser.errors, status=status.HTTP_401_UNAUTHORIZED)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_object(self):
        return self.request.user


class GetActivationEmailView(APIView):
    def post(self, request, *args, **kwargs):
        email: str = request.data['email']
        if helpers.is_valid_email(email):
            user = get_user_model().objects.filter(email=email).first()
            if user:
                user.activation_code = uuid.uuid4()
                user.save()
                data = {
                    'name': user.name,
                    'activation_code': user.activation_code
                }
                helpers.send_email(
                    'فعالسازی حساب کاربری گیزشاپ',
                    'verification_email.html',
                    'verification_text.txt',
                    data,
                    user.email
                )
                return Response({'result': 'success'}, status=status.HTTP_200_OK)
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'email is not valid'}, status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
    def get(self, request, activation_code=None):
        user = get_user_model().objects.filter(activation_code=activation_code).first()
        if user:
            user.is_active = True
            user.activation_code = None
            user.save()
            return Response({'result': 'success'}, status=status.HTTP_200_OK)
        # success redirect should add below
        return Response({'error': 'activation code is wrong'}, status=status.HTTP_400_BAD_REQUEST)


class GetResetEmailView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        if helpers.is_valid_email(email):
            user = get_user_model().objects.filter(email=email).first()
            if user:
                user.reset_code = random.randint(100000, 999999)
                user.save()
                print(user.reset_code)
                data = {
                    'reset_code': user.reset_code,
                    'name': user.name
                }
                helpers.send_email(
                    'بازیابی رمز عبور گیزشاپ',
                    'reset_email.html',
                    'reset_text.txt',
                    data,
                    user.email
                )
                return Response({'result': 'success'}, status=status.HTTP_200_OK)
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'email is not valid'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        reset_code = request.data['reset_code']
        new_password = request.data['password']
        user = get_user_model().objects.filter(reset_code=reset_code).first()
        if user:
            if len(new_password) < 6:
                return Response(
                    {'error': 'password must be greater than 6 characters'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(new_password)
            user.reset_code = None
            user.save()
            return Response({'result': 'success'}, status=status.HTTP_200_OK)
        return Response({'error': 'reset code is wrong'}, status=status.HTTP_400_BAD_REQUEST)


class ChangeLoginInfoView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            new_email = request.data['email']
        except KeyError:
            new_email = None

        try:
            new_password = request.data['new_password']
        except KeyError:
            new_password = None

        try:
            old_password = request.data['old_password']
        except KeyError:
            old_password = None

        if new_password:
            if not user.check_password(old_password):
                return Response({"error": 'Old Password Is Not Valid'})
            if len(new_password) < 6:
                return Response(
                    {'error': 'password must be greater than characters'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(new_password)
        if new_email:
            if len(new_email) > 0:
                if new_email != user.email:
                    if helpers.is_valid_email(new_email):
                        user.email = new_email
                        user.activation_code = uuid.uuid4()
                        user.is_active = False
                        data = {
                            'name': user.name,
                            'activation_code': user.activation_code
                        }
                        helpers.send_email(
                            'تغییر ایمیل کاربری',
                            'verification_email.html',
                            'verification_text.txt',
                            data,
                            user.email
                        )
                    else:
                        return Response(
                            {'error': 'email is not valid'}, status=status.HTTP_400_BAD_REQUEST
                        )
        user.save()
        return Response({'result': 'success'}, status=status.HTTP_200_OK)


# admin permissions


class ToggleUserActivationView(APIView):
    permission_classes = (custom_permissions.IsAdmin,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        user.is_active = not user.is_active
        user.save()
        return Response(
            {'result': f'{user} Enabled' if user.is_active else f'{user} Disabled'},
            status=status.HTTP_200_OK
        )


class GetAllUsersView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.AdminPanelUserSerializer
    permission_classes = (custom_permissions.IsAdmin,)
    authentication_classes = (authentication.TokenAuthentication,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'national_code', 'phone_number']
    ordering_fields = ['id', 'name', 'email']


class AdminManagesUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.AdminPanelUserSerializer
    permission_classes = (custom_permissions.IsAdmin,)
    authentication_classes = (authentication.TokenAuthentication,)


class AdminSetPasswordView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (custom_permissions.IsAdmin,)

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        user.set_password(request.data['password'])
        user.save()
        return Response({'result': 'success'}, status=status.HTTP_200_OK)
