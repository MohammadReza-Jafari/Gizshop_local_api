from django.urls import path

from . import views


urlpatterns = [
    path('send-email-to-all/', views.SendEmailToAll.as_view(), name='send_email_to_all'),
]
