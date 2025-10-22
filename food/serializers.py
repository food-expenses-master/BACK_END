from rest_framework import serializers

from food.models import Food
from food.service import format_collected_day


# FoodListSerializer:
# Food 모델 데이터를 API 응답 형태로 변환하는 Serializer.
class FoodListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category_display")
    day = serializers.SerializerMethodField()
    sales_region = serializers.CharField(source="get_region_display")
    rank = serializers.CharField(source="rank_name")
    sales_type = serializers.CharField(source="get_sales_type_display")

    class Meta:
        model = Food
        fields = [
            "id",
            "item_name",
            "price",
            "price_change_rate",
            "rank",
            "unit",
            "kind_name",
            "day",
            "category",
            "sales_type",
            "sales_region",
        ]

    # collected_date 기준으로 '당일 / n일전 / 1주일전' 등의 상대 날짜(day) 표시
    def get_day(self, obj):
        return format_collected_day(obj.collected_date)
