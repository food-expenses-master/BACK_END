from datetime import date
from django.utils import timezone

def format_collected_day(collected_date: date) -> str:
    """
    collected_date 기준으로 '당일 / n일전 / 1주일전 / 2주일전 / 1개월전 / 일년전' 라벨을 반환.
    출력 형식: "{라벨} (MM/DD)"
    """
    if collected_date is None:
        return ""

    today = timezone.now().date()
    diff = (today - collected_date).days

    if diff < 1:
        label = "당일"
    elif diff < 7:
        label = f"{diff}일전"
    elif diff == 7:
        label = "1주일전"
    elif diff < 15:
        label = "2주일전"
    elif diff < 32:
        label = "1개월전"
    else:
        label = "일년전"

    return f"{label} · ({collected_date.month}/{collected_date.day})"
