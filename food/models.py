from django.db import models

from food.choices import RegionType, FoodType, SalesType


class Food(models.Model):
    item_name = models.CharField(max_length=50)
    item_code = models.IntegerField()
    kind_name = models.CharField(max_length=20)
    kind_code = models.IntegerField()
    rank_name = models.CharField(max_length=20)
    rank_code = models.IntegerField()
    unit = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    collected_date = models.DateField()
    category = models.CharField(choices=FoodType, max_length=20)
    region = models.CharField(choices=RegionType, max_length=20)
    price_change_rate = models.CharField(max_length=10, blank=True, null=True)
    sales_type = models.CharField(choices=SalesType, max_length=10)
