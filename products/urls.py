from django.conf.urls import url
import views

urlpatterns = [
    url(r'^index/$', views.index, name="index"),
    url(r'^category/$', views.category, name="category"),
    url(r'^ship_cart/$', views.cart, name='cart'),
    url(r'^products_all/$', views.categories_all, name="categories_all"),
    url(r'^products_by_category/$', views.productsById, name="products_by_id"),
]
