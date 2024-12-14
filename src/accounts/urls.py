from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path

from accounts.views import (ChangeEmail, ChangeEmailActivation, ChangePassword,
                            EditProfile, Profile, ResetPassword,
                            ResetPasswordConfirm, UserActivation, UserLogin,
                            UserLogout, UserRegistration)

app_name = "accounts"
urlpatterns = [
    path("login/", UserLogin.as_view(), name="login"),
    path("reset-password/", ResetPassword.as_view(), name="reset_password"),
    path(
        "password-reset-confirm/<int:pk>/<token>/",
        ResetPasswordConfirm.as_view(),
        name="password_reset_confirm",
    ),
    path("register/", UserRegistration.as_view(), name="register"),
    path("profile/<int:pk>/", Profile.as_view(), name="profile"),
    path("profile/edit/<int:pk>/", EditProfile.as_view(), name="edit_profile"),
    path(
        "profile/edit/change_password/<int:pk>/",
        ChangePassword.as_view(),
        name="change_password",
    ),
    path("profile/edit/change_email/", ChangeEmail.as_view(), name="change_email"),
    path(
        "profile/edit/change_email/confirm/<int:pk>/<str:token>/",
        ChangeEmailActivation.as_view(),
        name="change_email_confirm",
    ),
    path("activate-user/<int:pk>/<str:token>/", UserActivation.as_view(), name="activate"),
    path("logout/", UserLogout.as_view(), name="logout"),
]
