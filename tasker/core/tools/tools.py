import datetime
import calendar

def days_left_in_month():
    today = datetime.date.today()
    _, days_in_month = calendar.monthrange(today.year, today.month)
    days_left = (datetime.date(
        today.year, today.month, days_in_month) - today).days
    return days_left