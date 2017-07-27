from django.conf.urls import url
from . import views
app_name = "pokeapp"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^poke/(?P<user_id>\d+)$', views.poke, name='poke'),
]