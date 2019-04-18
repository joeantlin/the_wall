from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^wall$', views.success),
    url(r'^postmessage$', views.message),
    url(r'^postcomment$', views.comment),
    url(r'^bye/(?P<type>\w+)/(?P<deleteid>\d+)$', views.delete),
    url(r'^logout$', views.logout),
]
