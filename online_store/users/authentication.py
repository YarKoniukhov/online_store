from users.models import User as User_profile
from users.models import User  # Убедитесь, что путь к вашей модели правильный


class EmailAuthBackend:
    """
    Аутентификация с использованием адреса электронной почты.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def create_profile(backend, user, *args, **kwargs):
    """
    Create user profile for social authentication
    """
    User_profile.objects.get_or_create(email=user.email)
