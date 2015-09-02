import requests
import json

client_id = "VEse61eNzmEA7onIXKGxGgwnaXLyqUJsZJ8ZlUSi"

# this shouldn't be exposed in version control but for this example
# I chose to just leave it here.  Ideally I could put it in settings.py which
# is already hidden, or just add a new keys.py and hide that.
client_secret = "uMiLj0X3DTd42MGE2dXDkX2rAlsoDV9hstInQtTEm8ALfI5P8oWY02lVfFDsJkawLciRIFR3TCd3XiZXIFcdfLzdfU0WjPbMj7C3OISDKk0KSULyLmB35b6tsnVOmymf"

def get_tokens(code):
    payload = {
        "grant_type":    "authorization_code",
        "client_id":     client_id,
        "client_secret": client_secret,
        "code":          code,
        "redirect_uri":  "http://localhost:8000/auth",
    }
    resp = requests.post("https://drchrono.com/o/token/", data=payload)
    parsed = json.loads(resp.text)
    return parsed

def get_patients(doctor, filters):
    headers = {
        "Authorization": "Bearer " + doctor.access_token
    }
    resp = requests.get("https://drchrono.com/api/patients", headers=headers,
            params=filters)
    parsed = json.loads(resp.text)
    return parsed["results"]
