# accounts/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authentication backend which allows users to authenticate using either their
    username or email address
    """
    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        UserModel = get_user_model()

        # If email is provided, use it
        if email:
            username = email

        try:
            # Try to fetch the user by searching the username or email field
            user = UserModel.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=username)
            ).first()

            # If the user was found, verify their password
            if user and user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            # No user was found with the given username/email
            return None

        # No user was found, or password validation failed
        return None