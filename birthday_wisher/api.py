import requests
import json
import datetime

client_id = "VEse61eNzmEA7onIXKGxGgwnaXLyqUJsZJ8ZlUSi"

# this shouldn't be exposed in version control but for this example
# I chose to just leave it here.  Ideally I could put it in settings.py which
# is already hidden, or just add a new keys.py and hide that.
client_secret = "uMiLj0X3DTd42MGE2dXDkX2rAlsoDV9hstInQtTEm8ALfI5P8oWY02lVfFDsJkawLciRIFR3TCd3XiZXIFcdfLzdfU0WjPbMj7C3OISDKk0KSULyLmB35b6tsnVOmymf"

# updates the token and expiry date for a given doctor
def refresh_tokens(doctor):
    payload = {
        "grant_type":    "refresh_token",
        "client_id":     client_id,
        "client_secret": client_secret,
        "refresh_token": doctor.refresh_token,
        "redirect_uri":  "http://localhost:8000/auth",
    }
    resp = requests.post("https://drchrono.com/o/token/", data=payload).json()
    return resp


# Refresh decorator
# Checks if the doctors token has expired and handles it if it does.
# All functions that call API endpoints should use this
def check_refresh(func):
    def check(*args, **kwargs):
        # assume the doctor is always the first argument
        # maybe change all methods to take kwargs so we dont have to make this
        # assumpion?
        doctor = args[0]
        if doctor.expires < datetime.date.today():
            new_tokens = refresh_tokens(doctor)
            doctor.access_token = new_tokens["access_token"]
            doctor.refresh_token = new_tokens["refresh_token"]
            doctor.expires = datetime.datetime.now() +\
                    datetime.timedelta(seconds=new_tokens["expires_in"])
            doctor.save()
        return func(*args, **kwargs)
    return check

# after obtaining the authorization code, this function requests the tokens
# needed to make API requests
def get_tokens(code):
    payload = {
        "grant_type":    "authorization_code",
        "client_id":     client_id,
        "client_secret": client_secret,
        "code":          code,
        "redirect_uri":  "http://localhost:8000/auth",
    }
    resp = requests.post("https://drchrono.com/o/token/", data=payload).json()
    return resp

# gets the list of all patients for a given doctor with optional filtering parameters
@check_refresh
def get_patients(doctor, filters = {}):
    headers = {
        "Authorization": "Bearer " + doctor.access_token
    }
    ret = []
    resp = requests.get("https://drchrono.com/api/patients", headers=headers,
            params=filters).json()
    while True:
        ret.extend(resp["results"])
        if resp["next"] is None:
            break
        resp = request.get(ret["next"], headers=headers, params=filters).json()
    return ret

# gets a list of appointments for the given doctor with optional filters
@check_refresh
def get_appointments(doctor, filters = {}):
    headers = {
        "Authorization": "Bearer " + doctor.access_token
    }
    resp = requests.get("https://drchrono.com/api/appointments", headers=headers,
            params=filters).json()
    return resp["results"]
