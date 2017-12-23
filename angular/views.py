# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from.service import getCompletedOrders, getUnCompletedOrders, get_order_by_ordersn, make_order
import json

from products.service import get_all_products, get_products_by_id, add_price_to_products
from customers.models import CustomerAddress

USER_ID = 12
# Create your views here.
def index(request):
    result = {}
    result['code'] = 1
    res = json.dumps(result)
    return HttpResponse(res.decode("unicode-escape"), content_type="application/json")
def categories(request):
    cgs = get_all_products()
    res = json.dumps(cgs)
    return HttpResponse(res.decode("unicode-escape"), content_type="application/json")
def category(request, category_id):
    cg = get_products_by_id(category_id)
    add_price_to_products(products=cg, city_id=3)#
    for product in cg:
        product['price'] = float('%.2f' % product['price']);
    res = json.dumps(cg)
    return HttpResponse(res.decode("unicode-escape"), content_type="application/json")
def completeOrders(request):
    if request.method == "GET":
        orders = getCompletedOrders()
        res = json.dumps(orders)
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")
def unCompleteOrders(request):
    if request.method == "GET":
        orders = getUnCompletedOrders()
        res = json.dumps(orders)
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")
def makeOrder(request):
    if request.method == "PUT":
        jsonStr = json.loads(request.body)
        user_id = USER_ID
        result = make_order(user_id=user_id, jsonStr=jsonStr)
        res = json.dumps(result)
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")

def orderDetail(reqeust, ordersn):
    if reqeust.method == 'GET':
        order = get_order_by_ordersn(ordersn=ordersn)
        res = json.dumps(order)
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")
def address(request):
    if request.method == 'GET':
        user_id = USER_ID
        l = CustomerAddress.objects.filter(user_id=user_id)
        res = {}
        if len(l) > 0:
            cuAddress = l[0]
            res['name'] = cuAddress.name
            res['phone'] = cuAddress.phone
            res['address'] = cuAddress.address
            res['doorNumber'] = cuAddress.door_number
            res['gender'] = '1' if cuAddress.sex else '2';
        res = json.dumps(res)
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")
    if request.method == "PUT":
        user_id = USER_ID
        received_json_data = json.loads(request.body)
        name = received_json_data['name']
        phone = received_json_data['phone']
        address  = received_json_data['address']
        door_number = received_json_data['doorNumber']
        gender = received_json_data['gender']
        sex = True if gender == '1' else False;

        result = {}
        try:
            customer_address = CustomerAddress.objects.filter(user_id= user_id)[0]
            customer_address.name = name
            customer_address.phone = phone
            customer_address.door_number = door_number
            customer_address.sex = sex
            customer_address.save()
            result['code'] = 0
        except IndexError:
            customer_address = CustomerAddress(name=name, phone=phone, address=address, door_number=door_number, sex=sex)
            customer_address.user_id = request.user.id
            customer_address.save()
            result['code'] = 1
        res = json.dumps(result)
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")
