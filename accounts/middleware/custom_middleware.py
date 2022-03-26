
import jwt, datetime
from django.conf import settings
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from accounts.models import User
from accounts.views import UserSerializer




class JsonWebTokenMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            # 토큰 HS256 알고리즘으로 디코딩
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()

        return self.get_response(request)
