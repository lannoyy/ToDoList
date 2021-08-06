from organisation.models import Organisation
from account.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import jwt
from drf_yasg.utils import swagger_auto_schema
from account.serializers import SignInSerializer


class CustomAuthorizationView(APIView):
    """
    View for authorization on jwt token
    """

    @swagger_auto_schema(responses={200: '{"token": string}'}, request_body=SignInSerializer)
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        organisation = get_object_or_404(Organisation, name=request.data['organisation']) 
        user = authenticate(username=username, password=password)
        data = {}
        if user and organisation in user.organisations.all():
            data['token'] = jwt.encode(
                {'user': user.get_username(), 'organisation': organisation.name},
                'secret', algorithm='HS256'
            )
        return Response(data)


class CustomAuthentication(authentication.BaseAuthentication):
    """
    Authentication on jwt token
    """
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return None

        try:
            data = jwt.decode(
                token, 'secret', algorithms='HS256'
            )
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid token')

        try:
            user = CustomUser.objects.get(username=data['user'])
        except CustomUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)
