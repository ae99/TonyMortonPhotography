from django.conf.urls import url
from photos import views

urlpatterns = [
    url(r'^$', views.index, name='index'),  # Handels calls to /photos/
    url(r'^photo/(?P<photo_id>[\w\-]+)/$', #Regex to select gallery item and its id
        views.show_photo, name='photo'),  #Sends to tag view to be handled
    url(r'^gallery/(?P<category_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^newPhoto/$', views.newPhoto, name="newPhoto"),
    url(r'^editPhoto/$', views.editPhoto, name="editPhoto"),
    url(r'^about/$', views.about, name='about'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
