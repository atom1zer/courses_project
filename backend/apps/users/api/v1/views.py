from apps.users.api.v1.serializers import (
    UserSerializer,
    VerifyAccountSerializer,
    UserSignInSerializer,
    PasswordResetSerializer,
)
from apps.users.models import User
from core.utils.utils import (
    generate_and_send_verification_email,
    generate_and_send_password_reset_email,
    get_user_by_uidb64,
)
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpRequest, HttpResponse, Http404
from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema_view, extend_schema
from drf_standardized_errors.openapi_serializers import Error401Serializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest) -> HttpResponse:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        generate_and_send_verification_email(user)
        return Response(
            _(
                "You have successfully signed up. Verification link has been sent to your email."
            ),
            status=status.HTTP_201_CREATED,
        )


class VerifyAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest, uidb64) -> HttpResponse:
        serializer = VerifyAccountSerializer(
            data={"uidb64": uidb64, "code": request.data["code"]}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            _("You successfully verified your account."),
            status=status.HTTP_200_OK,
        )


class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest) -> HttpResponse:
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=email, password=password)
        if user:
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response(
                    _("You need to verify your account first."),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            _("Invalid credentials."),
            status=status.HTTP_401_UNAUTHORIZED,
        )


class SignOutView(APIView):

    def delete(self, request):
        request.user.auth_token.delete()
        return Response(_("You signed out."), status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user = User.objects.get(email=request.data.get("email"))
            generate_and_send_password_reset_email(user)
            return Response(
                _("Password reset link has been sent to your email."),
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                _("No user found with this email."),
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        user = get_user_by_uidb64(uidb64)
        has_token = default_token_generator.check_token(user, token)

        if user is not None and has_token:
            serializer = PasswordResetSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                _("Password successfully changed."), status=status.HTTP_200_OK
            )
        else:
            return Response(_("Invalid link."), status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["User_details"])
@extend_schema_view(
        get=extend_schema(
            summary="Получить информацию о пользователе по токену",
            request=UserSerializer,
            responses={
                200: UserSerializer,
                401: Error401Serializer
            }
        ),
    )
class UserDetailsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            user = Token.objects.get(key=request.auth.key).user
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            raise Http404