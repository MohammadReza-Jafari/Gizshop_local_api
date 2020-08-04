from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.ManageUserView.as_view(), name='profile'),
    path('token/', views.GetAuthTokenView.as_view(), name='token'),
    path('activation-email/', views.GetActivationEmailView.as_view(), name='activation_email'),
    path('activate/<str:activation_code>/', views.ActivationView.as_view(), name='activate'),
    path('get-reset-code/', views.GetResetEmailView.as_view(), name='get_reset_code_email'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('change-login-info/', views.ChangeLoginInfoView.as_view(), name='change_login_info'),
    # admin permissions url
    path('all/', views.GetAllUsersView.as_view(), name='all_user'),
    path('toggle-user-activation/<int:pk>/', views.ToggleUserActivationView.as_view(), name='toggle_user_activation'),
    path('all/<int:pk>/', views.AdminManagesUserView.as_view(), name='manage_user'),
    path('set-password/<int:pk>/', views.AdminSetPasswordView.as_view(), name='set_password'),
]
