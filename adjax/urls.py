from django.conf.urls import url

from .views import dispatch, interface


urlpatterns = [
    url(r'^(?P<app>\w+)/(?P<name>\w+)$', dispatch, name='dispatch'),
    url(r'^interface\.js$', interface, name='interface'),
]
