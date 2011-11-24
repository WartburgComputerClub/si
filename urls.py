from django.conf.urls.defaults import patterns,include,url
from si.siadmin import site

urlpatterns = patterns('si.views',
    (r'^$','index'),                       
    (r'^signin/(?P<session>\d+)/$','signin'),
    (r'^admin/',include(site.urls)),
    (r'^register/$','register'),
    (r'^leave/$','leave'),                       
)
