from django.shortcuts import render

def index(req):
    return render(req, "birthday_wisher/index.html", {})
