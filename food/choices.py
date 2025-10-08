from django.db import models


# FoodType: 식품 분류를 이름(라벨)으로 관리하기 위한 enum 클래스
class FoodType(models.TextChoices):
    FRUIT = "fruit", "과일"
    GRAIN = "grain", "곡물/견과"
    SEAFOOD = "seafood", "수산물"
    MEAT = "meat", "고기"
    RED_PEPPER = "red_pepper", "고추류"
    CABBAGE = "cabbage", "배추류"
    VEGETABLE = "vegetable", "채소류"
    MUSHROOM = "mushroom", "버섯류"
    FOOD = "food", "식품"
    SAUCE = "sauce", "양념류"
    FRUIT_AND_VEGETABLE = "fruit/vegetable", "과채류"


# RegionType: 지역을 코드로 관리하기 위한 enum 클래스
class RegionType(models.TextChoices):
    ALL = "0000", "전체"
    SEOUL = "1101", "서울"
    BUSAN = "2100", "부산"
    DAEGU = "2200", "대구"
    INCHEON = "2300", "인천"
    GWANGJU = "2401", "광주"

    # 코드 -> 지역명 변환용 함수
    @classmethod
    def from_label(cls, label):
        return next((c.value for c in cls if c.label == label), None)


# SalesType: 판매처를 코드로 관리하기 위한 enum 클래스
class SalesType(models.TextChoices):
    RETAIL = "01", "소매"
    WHOLE = "02", "도매"

    # 코드 -> 지역명 변환용 함수
    @classmethod
    def from_label(cls, label):
        return next((c.value for c in cls if c.label == label), None)
