from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', views.home),
    url(r'^login/$', login , {'template_name': 'leave/index.html'}),
    url(r'^about/$', views.about),
    url(r'^incorrectinfo/$', views.incorrectinfo),
    url(r'^auth/$', views.auth),
    url(r'^loggedout/$', views.loggedout),
    url(r'^newleave/$', views.newleave),
    url(r'^confirmleave/$', views.confirmleave),
    url(r'^viewleaves/$', views.viewleaves),
    url(r'^sanction/$', views.sanction),
    url(r'^insufficientleaves/$', views.insufficientleaves),
    url(r'^approveleave/$', views.approveleave),
    url(r'^rejectapplication/$', views.rejectapplication),
    url(r'^rejectleave/$', views.rejectleave),
    url(r'^confirmsanction/$', views.confirmsanction),
    url(r'^confirmapplication/$', views.confirmapplication),
    url(r'^forwardsanction/$', views.forwardsanction),
    url(r'^forwardapplication/$', views.forwardapplication),
    url(r'^deleteleave/$', views.deleteleave),
    url(r'^saveleave/$', views.saveleave),
    url(r'^leavereject/$', views.leavereject)
    ]
