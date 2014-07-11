from django.conf.urls import patterns, url


urlpatterns = patterns(
    'adjax.views',

    url(r'^(?P<app>\w+)/(?P<name>\w+)$', 'dispatch', name='dispatch'),
    url(r'^interface\.js$', 'interface', name='interface'),
)
