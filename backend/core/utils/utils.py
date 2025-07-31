from typing import Any, Dict
import random, redis, os
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.safestring import SafeText
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.response import Response
from rest_framework import status

from apps.users.models import (
    User,
)
from apps.courses.models import (
    Lessons_Materials,
    Section_Lessons,
)
from apps.courses.api.v1.serializers import (
    Lessons_MaterialsSerializer,
)

from celery import shared_task

from django.core.files import File


REDIS_CODE_EXPIRY = 600

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")

redis_conn = redis.Redis(host=redis_host, port=redis_port)


def set_user_code_to_redis(user, code):
    user_key = f"topts:{user}:code"
    redis_conn.setex(user_key, REDIS_CODE_EXPIRY, code)


def get_user_code_from_redis(user):
    user_key = f"topts:{user}:code"
    topt_code = redis_conn.get(user_key)

    if topt_code:
        return topt_code.decode("utf-8")
    else:
        return None


@shared_task()
def send_email_to_user(
    subject: str, template: SafeText, email: Dict[str, Any], message: str = ""
) -> None:
    verification_email = EmailMultiAlternatives(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
    )
    verification_email.attach_alternative(template, "text/html")
    verification_email.send()
    

def get_encoded_user_pid(public_id):
    return urlsafe_base64_encode(force_bytes(public_id))


def get_user_by_uidb64(uidb64) -> User | None:
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        return User.objects.get(public_id=uid)
    except:  # (TypeError, ValueError, OverflowError, Users.DoesNotExist):
        return None


def generate_and_send_verification_email(user: User) -> None:
    totp = str(random.randint(100000, 999999))
    uidb64 = get_encoded_user_pid(user.public_id)
    link = f"frontend/verify/{uidb64}"  # f"{settings.FRONTEND_URL}/verify/{uidb64}"

    set_user_code_to_redis(user.email, totp)

    subject = "Code Verification"
    template = render_to_string(
        "emails/verification_email.html", {"totp": totp, "link": link}
    )

    send_email_to_user.delay(subject, template, user.email)


def generate_and_send_password_reset_email(user: User) -> None:
    totp = str(random.randint(100000, 999999))
    uidb64 = get_encoded_user_pid(user.public_id)
    link = f"frontend/resetpass/{uidb64}"  # f"{settings.FRONTEND_URL}/verify/{uidb64}"

    set_user_code_to_redis(user.email, totp)

    subject = "Password Reset"
    template = render_to_string(
        "emails/verification_email.html", {"totp": totp, "link": link}
    )

    send_email_to_user.delay(subject, template, user.email)

    token = default_token_generator.make_token(user)
    uidb64 = get_encoded_user_pid(user.public_id)
    link = f"frontend/reset-password/{uidb64}/{token}"  # f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{token}"

    subject = "Password Reset"
    template = render_to_string("emails/reset_password_email.html", {"link": link})

    send_email_to_user.delay(subject, template, user.email)

# @shared_task
# def upload_file_to_s3(file_path,public_id):
#     try:
#         with open(file_path, 'rb') as f:
#             django_file = File(f, name=os.path.basename(file_path))
#             foreign_object = Section_Lessons.objects.get(public_id=public_id)
#             Lessons_Materials.objects.create(lesson=foreign_object,content=django_file)
#         os.remove(file_path) # Clean up temporary file
#     except Exception as e:
#         # Handle errors
#         print(f"Error processing file: {e}")

def upload_file_to_s3(file_path,public_id):
    try:
        with open(file_path, 'rb') as f:
            django_file = File(f, name=os.path.basename(file_path))
            foreign_object = Section_Lessons.objects.get(public_id=public_id)
            new_file = Lessons_Materials.objects.create(lesson=foreign_object,content=django_file)
        new_file.url= new_file.content.url
        new_file.save()
        # os.remove(file_path) # Clean up temporary file
    except Exception as e:
        # Handle errors
        print(f"Error processing file: {e}")