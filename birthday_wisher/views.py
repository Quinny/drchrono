from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from . import api
from models import Doctor
from . import utils

def require_login(func):
    def check(*args, **kwargs):
        req = args[0]
        if 'user' not in req.session:
            return redirect("/")
        return func(*args, **kwargs)
    return check

# Since the dr chrono /api/patients endpoint date_of_birth filter doesn't support
# filtering by only day and month, I have to pull all the users and check if
# their birthday is today
def index(req):
    if 'user' in req.session:
        d = utils.get_doctor(req.session['user'])
        patients = utils.todays_birthdays(d)
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

@require_login
def next_appointment(req, patient_id):
    d = utils.get_doctor(req.session['user'])
    now = datetime.datetime.now()
    filters = {
        "patient":    patient_id,
        "date_range": utils.date_range(now, now + datetime.timedelta(days=180))
    }
    appts = api.get_appointments(d, filters)
    if not appts:
        appts.append({})
    return HttpResponse(json.dumps(appts[0]), content_type="application/json")

@csrf_exempt
@require_login
def add_note(req):
    if req.method == "POST":
        d = utils.get_doctor(req.session['user'])
        resp = api.patch_appointments(d, req.POST)
        return HttpResponse(json.dumps(resp), content_type="application/json")
    return redirect("/")
