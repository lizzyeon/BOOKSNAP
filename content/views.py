from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from uuid import uuid4
from .models import Feed, Like, Reply, Bookmark, Follow
from user.models import User
import os
from BOOKSNAP.settings import MEDIA_ROOT


class Main(APIView):    # /main 페이지를 보여줘라
    def get(self, request):                               # 페이지를 열 때(get) 실행되는 함수

        if not request.user.is_authenticated:                       # request.user는 authenticated(로그인 된) 상태인가?
            return render(request, "user/login.html")  # 로그인 안됐으면 로그인 페이지로 보내라

        user = request.user
        email = user.email

        feed_object_list = Feed.objects.all().order_by('-id')      # feed 테이블의 모든(all) 데이터(objects)를 가져옴.
        following_list = Follow.objects.filter(follower_email=email).values_list('following_email', flat=True)

        # 피드 구성
        feed_list = []       # feed, user, reply 등 데이터를 하나로 묶어 담을 리스트. 이것들이 합쳐서 하나의 피드를 만듦

        for feed in feed_object_list:
            feed_user = User.objects.filter(email=feed.email).first()   # 게시물 작성자 정보 가져오기
            if not feed_user:  # 혹시 작성자 정보가 없는 경우를 대비한 방어 코드
                continue

            reply_object_list = Reply.objects.filter(feed_id=feed.id)   # 이 게시물에 달린(feed_id가 같은) 댓글 가져오기
            is_followed = feed.email in following_list

            # 댓글 구성
            reply_list = []

            for reply in reply_object_list:
                reply_user = User.objects.filter(email=reply.email).first()
                if reply_user:
                    reply_list.append(dict(nickname=reply_user.nickname, reply_content=reply.reply_content))

            # 좋아요 처리
            like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()             # 좋아요 총 개수
            is_liked = Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists() # 사용자의 좋아요 누름 여부
            is_marked = Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()

            # feed_list(하나의 피드) 구성 요소
            feed_list.append(dict(id=feed.id,
                                  image=feed.image,
                                  content=feed.content,
                                  like_count=like_count,
                                  profile_image=feed_user.profile_image,
                                  nickname=feed_user.nickname,
                                  reply_list=reply_list,
                                  is_liked=is_liked,
                                  is_marked=is_marked,
                                  is_followed=is_followed))

        # 정상 로그인 상태면 Main 렌더링
        return render(request, "BOOKSNAP/MAIN.html", {"feeds": feed_list, "user" : user})


class UploadFeed(APIView):
    def post(self, request):

        # 데이터 꺼내기
        file = request.FILES.get('file')

        # 파일 이름 생성
        uuid_name = uuid4().hex                          # 랜덤 파일이름 생성
        extension = os.path.splitext(file.name)[1]       # 파일이름과 확장자 분리해서 확장자[1] 가져오기(.jpg .png)
        save_name = uuid_name + extension

        # 'media'에 파일 저장
        save_path = os.path.join(MEDIA_ROOT, save_name)  # 파일 저장 위치 : /project/media/save_name

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():                  # 작은 조각으로 나눠 저장(이미지는 용량이 크기 때문)
                destination.write(chunk)

        image = save_name
        content = request.data.get('content')
        email = request.session.get('email', None)

        # DB 저장
        Feed.objects.create(image=save_name, content=content, email=email)

        # '성공했다'고 브라우저에 알려줌
        return Response(status=200)


class MySnap(APIView):
    def get(self, request, nickname):

        if not request.user.is_authenticated:
            return render(request, "user/login.html")

        profile_user = User.objects.filter(nickname=nickname).first()

        if profile_user is None:
            return Response(status=404)

        email = profile_user.email

        is_followed = Follow.objects.filter(follower_email=request.user.email,   # 로그인한 유저가
                                            following_email=profile_user.email,  # 해당 유저를
                                            is_followed=True).exists()           # 현재 팔로우 상태(True)인 것만 filter

        # 내 게시물 | 좋아요 게시물 | 북마크 게시물
        feed_list = Feed.objects.filter(email=email).all().order_by('-id')
        like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True))
        like_feed_list = Feed.objects.filter(id__in=like_list).order_by('-id')
        bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list).order_by('-id')

        # 게시물 수 | 팔로워 수 | 팔로잉 수
        feed_count = Feed.objects.filter(email=email).count()
        follower_count = Follow.objects.filter(follower_email=email, is_followed=True).count()
        following_count = Follow.objects.filter(following_email=email, is_followed=True).count()

        # html로 데이터 전달
        return render(request, 'content/mysnap.html', context=dict(feed_list=feed_list,
                                                                                like_feed_list=like_feed_list,
                                                                                bookmark_feed_list=bookmark_feed_list,
                                                                                profile_user=profile_user,  # 프로필 주인
                                                                                login_user=request.user,    # 로그인한 유저
                                                                                feed_count=feed_count,
                                                                                follower_count=follower_count,
                                                                                following_count=following_count,
                                                                                is_followed=is_followed))


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        email = request.session.get('email', None)
        reply_content = request.data.get('reply_content', None)

        Reply.objects.create(feed_id=feed_id, email=email, reply_content=reply_content)

        return Response(status=200)


class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)                      # 좋아요 누른 피드
        email = request.session.get('email', None)                       # 누른 사람

        like, created = Like.objects.get_or_create(feed_id=feed_id, email=email, defaults={'is_liked':True})

        if not created:
            like.is_liked = not like.is_liked
            like.save()

        return Response(status=200)


class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        email = request.session.get('email', None)

        bookmark, created = Bookmark.objects.get_or_create(feed_id=feed_id, email=email, defaults={'is_marked':True})

        if not created:
            bookmark.is_marked = not bookmark.is_marked
            bookmark.save()

        return Response(status=200)


class ToggleFollow(APIView):
    def post(self, request):
        following_email = request.data.get('following_email', None)        # 팔로우 대상
        follower_email = request.user.email                                # 팔로우 누른 사람(로그인 사용자)

        if not follower_email:
            return Response({'error':'로그인이 필요합니다.'}, status=401)

        if not following_email:
            return Response({'error':'대상 유저가 없습니다.'}, status=400)

        if following_email == follower_email:
            print("❌ 자기 자신 팔로우 시도됨")
            return Response({'error':'자기 자신은 팔로우할 수 없습니다.'}, status=400)

        # 중복 확인
        follow, created = Follow.objects.get_or_create(following_email=following_email, # created(만들어진 게) 있나?
                                                       follower_email=follower_email,   # 있으면 get(가져오고)
                                                       defaults={'is_followed':True})   # 없으면 create(True를 defaults로 만들어라)
        if not created:
            follow.is_followed = not follow.is_followed
            follow.save()

        return Response({"is_followed": follow.is_followed},status=200)


