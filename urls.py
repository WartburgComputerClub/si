from django.conf.urls.defaults import patterns,include,url
from si.siadmin import site
from django.contrib.auth import views as auth_views
urlpatterns = patterns('si.views',
    url(r'^$','index',name='index'),                       
    (r'^signin/(?P<session>\d+)/$','signin'),
    (r'^admin/',include(site.urls)),
    (r'^register/$','register'),
    (r'^leave/$','leave'),                       
url(r'^passreset/$',auth_views.password_reset,{'template_name': 'si/password_reset_form.html'},name='forgot_password1'),
url(r'^passresetdone/$',auth_views.password_reset_done,{'template_name':'si/password_reset_done.html'},name='forgot_password2'),
url(r'^passresetconfirm/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$',auth_views.password_reset_confirm,{'template_name':'si/password_reset_confirm.html'},name='forgot_password3'),
url(r'^passresetcomplete/$',auth_views.password_reset_complete,{'template_name':'si/password_reset_complete.html'},name='forgot_password4'),
)
