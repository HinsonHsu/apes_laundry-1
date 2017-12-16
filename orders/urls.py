from django.conf.urls import url
import views

urlpatterns = [
    url(r'^index/$', views.index, name="index"),
    url(r'^make_order/$', views.make_order, name="make_order"),
    url(r'^cancel_order/$', views.cancel_order, name="cancel_order"),

]
