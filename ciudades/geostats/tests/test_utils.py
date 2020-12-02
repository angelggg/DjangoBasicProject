from django.contrib.auth.models import User


def create_get_test_user() -> User:
    user = User.objects.create(
                                email="test@tesmail.com",
                                first_name="test",
                                id=110,
                                password="test",
                                username="tes1t"
                                )
