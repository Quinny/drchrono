from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^add_note/?',              views.add_note),
    url(r'^next_appointment/(.*)/?', views.next_appointment),
    url(r'^auth',                    views.auth),
    url(r'^/?',                      views.index),
]
