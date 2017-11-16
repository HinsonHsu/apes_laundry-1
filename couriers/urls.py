from django.conf.urls import url
import views

urlpatterns = [
    url(r'^index/$', views.index, name="index"),
    url(r'^login/$', views.login, name='login'),
    url(r'^code/$', views.code, name="captcha"),

    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^test/$', views.test, name='test'),
    url(r'^map/$', views.map, name='map'),
    url(r'^upload/$', views.upload, name='upload'),
]