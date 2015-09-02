from django import template
from datetime import date, datetime
register = template.Library()

@register.filter(name='age')
def calculate_age(value):
    d = map(int, value.split("-"))
    born = datetime(d[0], d[1], d[2])
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

@register.filter(name='not_provided')
def not_provided(value):
    if len(value) > 0:
        return value
    return "Not provided"
