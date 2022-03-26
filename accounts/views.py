from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from django.conf import settings


class RegisterView(APIView):
#     {
#         "name": "a3",
#         "email": "a3@a.com",
#         "password": "a3"
#     }

    def post(self, request):
        # request의 data를 serializer에 넘긴다
        serializer = UserSerializer(data=request.data)
        # serializer를 validate한다
        # validation 에러나면 exception
        serializer.is_valid(raise_exception=True)
        # serializer 저장
        serializer.save()

        # serializer.save() : 유효성 검사를 통과한 값들을 저장
        # self.instance 존재 여부 : update(), create()


        # Response 객체로 전달되는 데이터를 클라이언트가 요청한 콘텐트 타입에 맞게 자동으로 렌더링 해준다.
        # 이는 @api_view 데코레이터가 Response 객체에 적절한 context를 가미하여 처리해준 결과이다.

        ### Unlike regular HttpResponse objects, you do not instantiate Response objects with rendered content.
        # Instead you pass in unrendered data, which may consist of any Python primitives.

         ###The renderers used by the Response class cannot natively handle complex datatypes such as Django model instances,
        # so you need to serialize the data into primitive datatypes before creating the Response object.


        return Response(serializer.data)

# {
#     "email":"a2@a.com",
#     "password": "a2"
# }
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZXhwIjoxNjQ3Mjc2NDUxLCJpYXQiOjE2NDcyNzI4NTF9.P4uK_EkpQdSZx8Iv54NMUcINS4IrGGrXkOtzoeUVFFE
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first() # unique 하기 때문에 first() # 에러를 raise할 수 있는 동작 404가 아니라 다른 것 없으면 None
        if user is None:
            raise AuthenticationFailed('User not found')

        # 패스워드 비교
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp' : datetime.datetime.now() + datetime.timedelta(minutes=60 * 24 * 300),
            'iat' : datetime.datetime.now()
        }

        # token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


        # return Response(user): Object of type User is not JSON serializable

        # 로그인 유저는 jwt를 보내서 로그인에 사용한다
        # 토킅을 쿠키을 통해 전
        response = Response()

         #  """
         # if httponly:
         #    self.cookies[key]['httponly'] = True
         #  """
        # httponly에 저장



        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data =  {
            'jwt': token,
        }
        return response


### authenticated user
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZXhwIjoxNjQ3Mjc2NDUxLCJpYXQiOjE2NDcyNzI4NTF9.P4uK_EkpQdSZx8Iv54NMUcINS4IrGGrXkOtzoeUVFFE
# 미들웨어 : 유저를 인증하는 과정
class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            # 토큰 HS256 알고리즘으로 디코딩
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        # token의 payload에 있는 user id로 user 찾음
        user = User.objects.filter(id=payload['id']).first()
        # 받은 아이디로 시리얼라이즈
        serializer = UserSerializer(user)
        return Response(serializer.data)



class LogoutView(APIView):
    def post(self, request):
        response = Response()
        # 쿠키에서 jwt 지운다
        response.delete_cookie('jwt') # 작동 안함 , max_age=0이 더 정확
        response.data = {
            'message': 'success'
        }
        return response