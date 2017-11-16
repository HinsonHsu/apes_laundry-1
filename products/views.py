# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from .service import get_all_products, get_products_by_id, get_category_by_id
# Create your views here.
import json


@csrf_exempt
def index(request):
    return render(request,"products/index.html")

@csrf_exempt
def category(request):
    return render(request, "products/category.html")

@csrf_exempt
def categories_all(request):
    result = {}
    products = get_all_products()
    result["result"] = "success"  # 1成功
    result["code"] = 1
    result["data"] = products
    res = json.dumps(result)
    print res.decode("unicode-escape")
    return HttpResponse(res.decode("unicode-escape"), content_type="application/json")

def productsById(request):
    category_id = request.GET.get('category_id')
    result = {}
    print category_id
    products = get_products_by_id(category_id)
    result["result"] = "success"  # 1成功
    result["code"] = 1
    result["data"] = products
    result['category'] = get_category_by_id(category_id)[0]['name']
    res = json.dumps(result)
    print res.decode("unicode-escape")
    return HttpResponse(res.decode("unicode-escape"), content_type="application/json")