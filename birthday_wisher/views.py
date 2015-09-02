from django.shortcuts import render
from . import api

def index(req):
    context = {
        "client_id": api.client_id,
    }
    return render(req, "birthday_wisher/index.html", context)
