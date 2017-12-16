from django.conf.urls import url
import views

urlpatterns = [
    url(r'^index/$', views.index, name="index"),
    url(r'^login/$', views.login, name='login'),
    url(r'^code/$', views.code, name="captcha"),

    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^unaccepted_orders/$', views.notAccepted_orders, name='unaccepted_orders'),
    url(r'^accepted_orders/$', views.accepted_orders, name='accepted_orders'),
    url(r'^complete_orders/$', views.complete_orders, name='complete_orders'),
    url(r'^personal/$', views.personal, name='personal'),
    url(r'^order_detail/$', views.orderDetail, name='order_detail'),
]