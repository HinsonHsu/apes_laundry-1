# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from .service import get_all_products, get_products_by_id, get_category_by_id, getCities, get_products_by_city, add_price_to_products
# Create your views here.
import json


@csrf_exempt
def index(request):
    addresses = getCities()
    return render(request,"products/index.html", {"addressList": addresses})

@csrf_exempt
def category(request):
    addresses = getCities()
    return render(request, "products/category.html",{"addressList": addresses})
def cart(request):
    return render(request, 'products/ship_cart.html')

@csrf_exempt
def categories_all(request):
    result = {}
    city_id = request.GET.get('city_id')
    print "city_id:{0}".format(city_id)
    # products = None
    # if city_id == -1:
    #     print "city_id:{0}".format(city_id)
    #     products = get_all_products()
    # else:
    products = get_products_by_city(city_id)
    result["result"] = "success"  # 1成功
    result["code"] = 1
    result["data"] = products
    res = json.dumps(result)
    print res.decode("unicode-escape")
    return HttpResponse(res.decode("unicode-escape"), content_type="application/json")

def productsById(request):
    from .service import check_category_and_city
    category_id = request.GET.get('category_id')
    city_id = request.GET.get('city_id')
    print category_id, city_id
    result = {}
    if check_category_and_city(category_id,city_id):
        products = get_products_by_id(category_id)
        products = add_price_to_products(products, city_id)
        result["data"] = products
    else:
        result["data"] = []
    result["result"] = "success"  # 1成功
    result["code"] = 1

    result['category'] = get_category_by_id(category_id)[0]['name']
    res = json.dumps(result)
    print res.decode("unicode-escape")
    return HttpResponse(res.decode("unicode-escape"), content_type="application/json")