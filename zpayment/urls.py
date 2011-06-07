from django.conf.urls.defaults import patterns, url

from zpayment.views import result, success, fail

urlpatterns = patterns('',
    url(r'^result/$', result, name='zpayment-result'),
    url(r'^success/$', success, name='zpayment-success'),
    url(r'^fail/$', fail, name='zpayment-fail'),
)
