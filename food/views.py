from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from food.serializers import FoodListSerializer
from food.choices import SalesType, RegionType
from food.models import Food


# FoodListGenericAPIView:
# Food 모델 데이터를 조회하는 APIView.
class FoodListGenericAPIView(GenericAPIView, ListModelMixin):
    queryset = Food.objects.all()
    serializer_class = FoodListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        qs = super().get_queryset()
        sales_type = self.request.query_params.get("sales_type", None)
        region = self.request.query_params.get("region", None)

        # sales_type(판매유형), region(지역) 쿼리파라미터로 필터링
        if sales_type:
            sales_type = SalesType.from_label(sales_type)
            # 유효하지 않은 값이면 400 코드와 에러 응답 반환
            if not sales_type:
                raise ValidationError("WRONG_SALES_TYPE")
            qs = qs.filter(sales_type=sales_type)

        region_code = "0000"
        if region:
            region_code = RegionType.from_label(region)
            # 유효하지 않은 값이면 400 코드와 에러 응답 반환
            if not region_code:
                raise ValidationError("WRONG_REGION")

        return qs.filter(region=region_code)

    def get(self, request, *args, **kwargs):
        try:
            qs = self.get_queryset()
        except ValidationError as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "success": False,
                    "code": str(e.detail[0]),
                    "data": {},
                },
            )

        serializer = self.get_serializer(qs, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data={
                "success": True,
                "code": "OK",
                "data": serializer.data,
            },
        )
