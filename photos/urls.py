from django.conf.urls import url
from photos import views

urlpatterns = [
    url(r'^$', views.index, name='index'),  # Handels calls to /photos/

    url(r'^gallery/$', views.index, name='index'),  # Handels calls to /gallery/


    url(r'^tag/(?P<tag_name_slug>[\w\-]+)/$', #Regex to select tag and its slug
        views.show_tag, name='show_tag'),  #Sends to tag view to be handled

    url(r'^gallery/(?P<photo_name_slug>[\w\-]+)/$', #Regex to select gallery item and its slug
        views.show_photo, name='photo'),  #Sends to tag view to be handled


    url(r'^addPhoto/$', views.add_photo, name="addPhoto"),
    url(r'^about/$', views.about, name='about'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]

