from django import template
from datetime import date, datetime
import random
register = template.Library()

@register.filter(name='age')
def calculate_age(value):
    d = map(int, value.split("-"))
    born = datetime(d[0], d[1], d[2])
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

@register.filter(name='not_provided')
def not_provided(value):
    if value:
        return value
    return "Not provided"

# Wouldn't actually be used, but all of the provided images 404, so this
# is just a place holder
@register.filter(name='fake_image')
def fake_image(person):
    genders = {
        "Male":   "men",
        "Female": "women",
    }
    if not person["gender"]:
        person["gender"] = "Female"
    return "http://api.randomuser.me/portraits/med/" +\
            genders[person["gender"]] +\
            "/" + str(person["id"] % 90) + ".jpg"
