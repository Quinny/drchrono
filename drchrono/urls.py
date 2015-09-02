from django.conf.urls import include, url
import birthday_wisher

urlpatterns = [
    url(r'^.*', include('birthday_wisher.urls'))
    #    url(r'^admin/', include(admin.site.urls)),
]
