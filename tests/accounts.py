from django.contrib.auth import get_user_model


def create_random_accounts(number):
    return [get_user_model().objects.create(
            username=str(num) + 'testaccount',
            password=str(num) + 'testpassword',
            email=str(num) + '@example.com') for num in range(1, number+1)]
