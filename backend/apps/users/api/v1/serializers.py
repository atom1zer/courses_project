import redis
from apps.users.models import User
from core.utils.utils import get_user_by_uidb64, get_user_code_from_redis
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

redis_conn = redis.Redis(host="127.0.0.1", port=6379)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["public_id", "email", "name", "created", "updated", "password", "is_admin"]
        extra_kwargs = {
            "email": {
                "error_messages": {
                    "required": _("Email field is required."),
                    "invalid": _("Enter a valid email address."),
                    "unique": _(
                        "Account with such email address is alredy registered."
                    ),
                }
            },
            "name": {
                "required": True,
                "error_messages": {
                    "required": _("Name field is required."),
                    "invalid": _("Name contains invalid characters."),
                    "max_length": _("Name cannot be longer than 20 characters."),
                },
            },
            "password": {
                "write_only": True,
                "error_messages": {
                    "required": _("Password field is required."),
                    "invalid": _("Password should be stronger."),
                },
            },
            "is_admin": {"read_only": True},
            # "duration": {"write_only": True},
        
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"],
            validated_data["name"],
            validated_data["password"],
        )
        return user


class VerifyAccountSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(max_length=64)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        now = timezone.now()
        user = get_user_by_uidb64(attrs["uidb64"])

        if user is None:
            raise serializers.ValidationError(_("No account found"), code=404)

        if user.is_active:
            raise serializers.ValidationError(
                _("You already have verified your account")
            )

        user_code = get_user_code_from_redis(user.email)

        if user_code is None:
            raise serializers.ValidationError(_("Your code has expired."), code=400)

        if user_code != attrs["code"]:
            raise serializers.ValidationError(_("Code is invalid"), code=400)

        user.is_active = True
        user.save()

        return attrs


class UserSignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=3, write_only=True)
    # confirm_password = serializers.CharField(min_length=3, write_only=True)

    # def validate(self, data):
    #     if data['new_password'] != data['confirm_password']:
    #         raise serializers.ValidationError("Passwords do not match.")
    #     return data
