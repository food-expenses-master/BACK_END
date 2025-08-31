from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.exceptions import TokenError

from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserRegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        nickname = request.data.get("nickname", None)
        password = request.data.get("password", None)
        # nickname&password 검증
        if not nickname or not password:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "success": False,
                    "code": "NICKNAME_AND_PASSWORD_REQUIRED",
                    "data": {},
                }
            )

        try:
            User = get_user_model()
            User.objects.create_user()
        except:
            # User nickname이 중복된 경우
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "success": False,
                    "code": "DUPLICATE_NICKNAME",
                    "data": {},
                },
            )
        return Response(
            status=status.HTTP_200_OK,
            data={
                "success": True,
                "code": "OK",
                "data": {},
            },
        )


class UserAuthAPIView(APIView):
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated()]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        nickname = request.data.get("nickname", None)
        password = request.data.get("password", None)
        # nickname&password 검증
        if not nickname or not password:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "success": False,
                    "code": "NICKNAME_AND_PASSWORD_REQUIRED",
                    "data": {},
                }
            )

        try:
            user = User.objects.get(nickname=nickname)
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "success": False,
                    "code": "USER_NOT_FOUND",
                    "data": {},
                }
            )

        # password 체크
        if not check_password(password, user.password):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "success": False,
                    "code": "PASSWORD_NOT_MATCH",
                    "data": {},
                }
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        # 캐시에 Refresh_token 저장
        cache.set(key=f"refresh_token:{user.id}", value=refresh_token, timeout=7 * 24 * 3600)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "success": True,
                "code": "OK",
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
            },
        )
    def delete(self, request, *args, **kwargs):
        user = request.user
        # 캐시에 저장된 Refresh_token 삭제
        cache.delete(f"refresh_token:{user.id}")
        return Response(
            status=status.HTTP_200_OK,
            data={
                "success": True,
                "code": "OK",
                "data": {},
            },
        )


class TokenRefreshAPIView(APIView):
    # 토큰 refresh
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh = request.data.get("refresh", None)
        if not refresh or not type(refresh) is str:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"success": False, "code": "REFRESH_TOKEN_REQUIRED", "data": {}},
            )

        try:
            refresh_token = RefreshToken(refresh)
        except (TokenError):
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"success": False, "code": "INVALID_REFRESH_TOKEN", "data": {}},
            )

        return Response(
            status=status.HTTP_200_OK,
            data={
                "success": True,
                "code": "OK",
                "data": {"access_token": str(refresh_token.access_token)},
            },
        )