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

def index(req):
    if 'user' in req.session:
        d = get_doctor(req.session['user'])
        patients = filter(is_birthday, api.get_patients(d, {}))
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
