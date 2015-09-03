import datetime
from models import Doctor
from . import api

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
    patients = filter(is_birthday, api.get_patients(doctor))
    # just for testing
    #patients = filter(lambda x: x["date_of_birth"] is not None, api.get_patients(doctor))
    for p in patients:
        p["has_contact"] = p["home_phone"] or p["email"] or p["cell_phone"]
    return patients
