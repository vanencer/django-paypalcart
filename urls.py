from django.conf.urls.defaults import *

urlpatterns = patterns('django_paypalcart.views',
    (r'^checkout/$', 'checkout'),
    (r'^success/$',  'success'),
    (r'^cancel/$',   'cancel'),
    (r'^confirm/$',  'confirm'),
)
