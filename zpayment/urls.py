from django.conf.urls.defaults import patterns, url

from zpayment.views import result

urlpatterns = patterns('',
    url(r'^result/$', result, name='zpayment-result'),
    url(r'^success/$', result, name='zpayment-success'),
    url(r'^fail/$', result, name='zpayment-fail'),
)
