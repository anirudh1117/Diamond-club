from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)

def generate_password(name):

    password = "".join(name.split(' ')).lower()
    random_password = password + str(random.randint(100, 10000))
    return random_password


def register_social_user(provider, user_id, email, name,first_name,last_name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=os.environ.get('SOCIAL_SECRET'))

            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        username = generate_username(name)
        password = generate_password(name)
        user = {
            'username': username, 'email': email,
            'first_name':first_name,'last_name':last_name,
            'password': password}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()
        #new_user = authenticate(
            #username=username, password=password)
        #print(new_user)
        if user.email is None:
            email = None
        else:
            email = user.email
        token, created = Token.objects.get_or_create(user=user)
        return {
            'email':email,
            'username': user.username,
            'tokens': token.key
        }