from rest_framework import authentication, status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from . import helpers, permissions as custom_permissions


class SendEmailToAll(APIView):
    permission_classes = (custom_permissions.IsAdmin,)
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        emails = [user.email for user in get_user_model().objects.all()]
        subject = request.data['subject']
        message = request.data['message']
        data = {
            'message': message
        }
        try:
            helpers.send_email(
                subject,
                'send_email.html',
                'send_text.txt',
                data,
                emails
            )
            return Response({'result': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendEmailView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (custom_permissions.IsAdmin,)

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        subject = request.data['subject']
        message = request.data['message']
        data = {
            'message': message
        }

        try:
            helpers.send_email(
                subject,
                'send_email.html',
                'send_text.txt',
                data,
                user.email
            )
            return Response({'result': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
