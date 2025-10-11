from django.db import models


# FoodType: 식품 분류를 이름(라벨)으로 관리하기 위한 enum 클래스
class FoodType(models.TextChoices):
    FRUIT = "fruit", "과일"
    GRAIN = "grain", "곡물·견과"
    SEAFOOD = "seafood", "수산물"
    MEAT = "meat", "고기·단백질"
    RED_PEPPER = "red_pepper", "고추류"
    CABBAGE = "cabbage", "배추류"
    VEGETABLE = "vegetable", "채소류"
    MUSHROOM = "mushroom", "버섯류"
    FOOD = "food", "식품"
    SAUCE = "sauce", "양념류"
    FRUIT_AND_VEGETABLE = "fruit/vegetable", "과채류"


    # 타입명 -> 코드로 변환용 함수
    @classmethod
    def from_label(cls, label):
        return next((c.value for c in cls if c.label == label), None)


# RegionType: 지역을 코드로 관리하기 위한 enum 클래스
class RegionType(models.TextChoices):
    ALL = "0000", "전체"
    SEOUL = "1101", "서울"
    BUSAN = "2100", "부산"
    DAEGU = "2200", "대구"
    INCHEON = "2300", "인천"
    GWANGJU = "2401", "광주"
    DAEJEON = "2501", "대전"
    ULSAN = "2601", "울산"
    SUWON = "3111", "수원"
    GANGNEUNG = "3214", "강릉"
    CHUNCHEON = "3211", "춘천"
    CHEONGJU = "3311", "청주"
    JEONJU = "3511", "전주"
    POHANG = "3711", "포항"
    JEJU = "3911", "제주"
    UIJEONGBU = "3113", "의정부"
    SUNCHEON = "3613", "순천"
    ANDONG = "3714", "안동"
    CHANGWON = "3814", "창원"
    YONGIN = "3145", "용인"
    SEJONG = "2701", "세종"
    SEONGNAM = "3112", "성남"
    GOYANG = "3138", "고양"
    CHEONAN = "3411", "천안"
    GIMHAE = "3818", "김해"

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
