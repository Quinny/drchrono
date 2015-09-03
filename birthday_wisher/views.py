from django.shortcuts import render, redirect
import datetime

from . import api
from models import Doctor

def is_birthday(person):
    if person["date_of_birth"] is None:
        return False
    now = datetime.datetime.now()
    toks = person["date_of_birth"].split("-")
    return int(toks[1]) == now.month and int(toks[2]) == now.day

def get_doctor(pk):
    return Doctor.objects.get(pk=pk)

def date_range(d1, d2):
    return d1.isoformat() + "/" + d2.isoformat()

# gets todays birthdays for the given doctor
# also adds nessesary data to each user
def todays_birthdays(doctor):
    #patients = filter(is_birthday, api.get_patients(doctor))
    # just for testing
    patients = filter(lambda x: x["date_of_birth"] is not None, api.get_patients(doctor))
    now = datetime.datetime.now()
    for p in patients:
        if not p["home_phone"] and not p["email"] and not p["cell_phone"]:
            p["has_contact"] = False
            '''filters = {
                "patient":    p["id"],
                "date_range": date_range(now, now + datetime.timedelta(days=180))
            }
            x = api.get_appointments(doctor, filters)
            if x:
                p["next_appointment"] = x[0]["scheduled_time"]'''
        else:
            p["has_contact"] = True
    return patients

# Since the dr chrono /api/patients endpoint date_of_birth filter doesn't support
# filtering by only day and month, I have to pull all the users and check if
# their birthday is today
def index(req):
    if 'user' in req.session:
        d = get_doctor(req.session['user'])
        patients = todays_birthdays(d)
        context = {
                "patients": patients
        }
        return render(req, "birthday_wisher/people.html", context)

    context = {
        "client_id": api.client_id,
    }
    return render(req, "birthday_wisher/index.html", context)

def auth(req):
    tokens = api.get_tokens(req.GET.get("code", ""))
    expires = datetime.datetime.now() +\
            datetime.timedelta(seconds=tokens["expires_in"])
    d = Doctor.objects.create(
            access_token  = tokens["access_token"],
            refresh_token = tokens["refresh_token"],
            expires       = expires,
    )
    d.save()
    req.session['user'] = d.pk
    return redirect("/")
