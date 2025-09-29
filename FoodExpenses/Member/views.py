from django.contrib.auth.hashers import check_password
from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]

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
            with transaction.atomic():
                User.objects.create_user(nickname=nickname, password=password)
        except IntegrityError:
            return Response(
                status=status.HTTP_409_CONFLICT,
                data={"success": False, "code": "DUPLICATE_NICKNAME", "data": {}},
            )
        return Response(
            status=status.HTTP_201_CREATED,
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
                    "code": "INVALID_CREDENTIALS",
                    "data": {},
                }
            )

        # password 체크
        if not check_password(password, user.password):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "success": False,
                    "code": "INVALID_CREDENTIALS",
                    "data": {},
                }
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

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
        # 로그아웃 시 유저의 모든 리프레시 토큰 무효화
        tokens = OutstandingToken.objects.filter(user=request.user.id)
        for t in tokens:
            BlacklistedToken.objects.get_or_create(token=t)

        return Response(
            status=status.HTTP_200_OK,
            data={"success": True, "code": "OK", "data": {}},
        )


class TokenRefreshAPIView(APIView):
    # 토큰 refresh
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh = request.data.get("refresh_token", None)
        if not refresh or  not isinstance(refresh, str):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"success": False, "code": "REFRESH_TOKEN_REQUIRED", "data": {}},
            )

        # refresh 토큰 검증
        try:
            old_refresh = RefreshToken(refresh)
        except TokenError:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"success": False, "code": "INVALID_REFRESH_TOKEN", "data": {}},
            )

        # refresh 토큰 블랙리스트 등록
        try:
            old_refresh.blacklist()
        except Exception:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={"success": False, "code": "SERVER_ERROR", "data": {}},
            )

        user_pk = old_refresh.payload.get("user_id")
        try:
            user = User.objects.get(id=user_pk)
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"success": False, "code": "INVALID_REFRESH_TOKEN", "data": {}},
            )

        # 새 refresh 발급 및 access 동시 발급
        new_refresh = RefreshToken.for_user(user)
        new_access = str(new_refresh.access_token)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "success": True,
                "code": "OK",
                "data": {
                    "access_token": new_access,
                    "refresh_token": str(new_refresh),
                },
            },
        )
