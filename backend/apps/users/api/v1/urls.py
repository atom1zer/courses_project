from django.urls import path

from .views import (
    SignUpView,
    VerifyAccountView,
    SignInView,
    SignOutView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    UserDetailsView,
)

urlpatterns = [
    path(
        "sign-up",
        SignUpView.as_view(),
        name="sign-up",
    ),
    path(
        "verify/<uidb64>",
        VerifyAccountView.as_view(),
        name="verify",
    ),
    path(
        "sign-in",
        SignInView.as_view(),
        name="sign-in",
    ),
    path(
        "sign-out",
        SignOutView.as_view(),
        name="sign-out",
    ),
    path(
        "password-reset",
        PasswordResetRequestView.as_view(),
        name="password-reset",
    ),
    path(
        "password-reset/<uidb64>/<token>",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "user-details",
        UserDetailsView.as_view(),
        name="user-details-get",
    ),
]
