from django.conf.urls import url
import views

urlpatterns = [
    url(r'^index/$', views.index, name="index"),
    url(r'^categories/$', views.categories, name="categories"),
    url(r'^category/(\d+)$', views.category, name="category"),
    url(r'^uncompletedorders/$', views.unCompleteOrders, name="uncompletedorders"),
    url(r'^completedorders/$', views.completeOrders, name="completedorders"),
    url(r'^orderdetail/(\d+)$', views.orderDetail, name="orderdetail"),
    url(r'^useraddress/$', views.address, name="useraddress"),
    url(r'^makeorder/$', views.makeOrder, name="makeorder"),
]
