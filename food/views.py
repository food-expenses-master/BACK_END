from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from food.choices import RegionType, SalesType
from food.models import Food, Store
from food.serializers import FoodListSerializer
from food.service import format_collected_day


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


# FoodDetailAPIView
# Food 데이터 상세를 조회하는 APIView
class FoodDetailAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        # 대상 Food 단건 조회
        food = Food.objects.filter(id=pk).first()
        if not food:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"success": False, "code": "FOOD_NOT_FOUND", "data": {}},
            )

        # 동일 스펙(품목/품종/등급)인 WHOLE/RETAIL 두 종류를 한 번에 조회
        foods = (
            Food.objects.filter(
                item_code=food.item_code,
                kind_code=food.kind_code,
                rank_code=food.rank_code,
                sales_type__in=[SalesType.WHOLE, SalesType.RETAIL],
            )
            .values("sales_type", "price", "price_change_rate", "collected_date")
        )
        price_by_type = {row["sales_type"]: row for row in foods}
        whole = price_by_type.get(SalesType.WHOLE, {})
        retail = price_by_type.get(SalesType.RETAIL, {})
        wholesale_day= whole.get("collected_date") or None
        retail_day = retail.get("collected_date") or None

        food_data = {
            "item_name": food.item_name,
            "wholesale_price": whole.get("price") or 0,
            "wholesale_price_change_rate": whole.get("price_change_rate") or "-",
            "wholesale_day" : format_collected_day(wholesale_day) if wholesale_day else "-",
            "retail_price": retail.get("price") or 0,
            "retail_price_change_rate": retail.get("price_change_rate") or "-",
            "retail_day": format_collected_day(retail_day) if retail_day else "-",
            "rank": food.rank_name,
            "unit": food.unit,
            "category": food.get_category_display(),
            "sales_region": food.get_region_display(),
            "recommended_store": [],
        }

        # 단건 조회한 Food 지역이 서울인 경우 추천 가게 조회
        if food.region == RegionType.SEOUL.value:
            recommended = (
                Store.objects
                .filter(food_category__contains=[food.category])
                .values("name", "business_info", "image", "address", "address_link", "number")
            )
            food_data["recommended_store"] = list(recommended)

        return Response(
            status=status.HTTP_200_OK,
            data={"success": True, "code": "OK", "data": food_data},
        )
