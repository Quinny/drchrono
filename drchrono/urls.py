from django.conf.urls import include, url
from birthday_wisher import views

urlpatterns = [
    url(r'', include('birthday_wisher.urls'))
]
