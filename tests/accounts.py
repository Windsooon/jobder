from django.contrib.auth import get_user_model


def create_one_account():
    return get_user_model().objects.create_user(
            username='1testoneaccount',
            password='1testonepassword',
            email='1@oneexample.com')


def create_multi_accounts(number):
    return [get_user_model().objects.create_user(
            username=str(num) + 'testaccount',
            password=str(num) + 'testpassword',
            email=str(num) + '@example.com') for num in range(1, number+1)]
