from django.conf.urls import url
from photos import views


# Defines URL patterns - what view to send each url to
urlpatterns = [
    # Handels calls to '/', sends it to index view to be handeled
    url(r'^$', views.index, name='index'),
    url(r'^gallery/(?P<category_slug>[\w\-]+)/(?P<page_number>[\d]+)/$', views.index, name='index'),

    url(r'^new/$', views.newPhoto, name="newPhoto"),
    url(r'^edit/(?P<photo_id>[\d]+)/$', views.editPhoto, name='editPhoto'),
    url(r'^delete/(?P<photo_id>[\d]+)/$', views.deletePhoto, name='deletePhoto'),

    url(r'^categories/$', views.categories, name="categories"),

    url(r'^about/$', views.about, name='about'),

    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),


    # <photo_id> is Regular Expression (REGEX) to extract variable from URL
    url(r'^photo/(?P<photo_id>[\d]+)/$', views.show_photo, name='photo'),
]
