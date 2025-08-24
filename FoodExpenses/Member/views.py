from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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
                    "code" : "NICKNAME_AND_PASSWORD_REQUIRED"
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
                },
            )
        return Response(
            status=status.HTTP_200_OK,
            data={
                "success": True,
                "code": "OK",
            },
        )


