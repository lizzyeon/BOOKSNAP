import os
from uuid import uuid4
from BOOKSNAP.settings import MEDIA_ROOT
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from content.models import Follow
from .models import User

# 회원가입
class Join(APIView):
    def get(self,request):
        return render(request, "user/join.html")

    def post(self,request):
        email =  request.data.get('email', None)
        password = request.data.get('password', None)
        name = request.data.get('name', None)
        nickname = request.data.get('nickname', None)

        User.objects.create(email=email,
                            password=make_password(password),
                            name=name,
                            nickname=nickname,
                            profile_image="DEFAULT_IMAGE.png")

        return Response(status=200)

# 로그인
class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        print(f"현재 로그인한 유저: {request.user}")
        print(f"로그인 상태: {request.user.is_authenticated}")

        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=400, data=dict(message="회원정보를 다시 한 번 확인해주세요."))

        if user.check_password(password):
            login(request, user)
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="회원정보를 다시 한 번 확인해주세요."))

# 로그아웃
class LogOut(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "user/login.html")


class UploadProfile(APIView):
    def post(self, request):

        # 데이터 꺼내기
        file = request.FILES['file']
        email= request.data.get('email')

        uuid_name = uuid4().hex                             # 랜덤으로 이미지 이름 생성
        save_path = os.path.join(MEDIA_ROOT, uuid_name)     # media에 저장

        # ('media'에) 파일 저장
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name                           # 파일 이름을을 'profile_image' 필드에 저장

        user = User.objects.filter(email=email).first()        # 해당 이메일 주소를 찾아서
        user.profile_image = profile_image                  # 해당 사용자의 프로필 이미지에 '그' 파일을
        user.save()                                         # DB에 저장

        return Response(status=200)
