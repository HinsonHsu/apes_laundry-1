# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import json, math, time, random
from django.utils import timezone
import datetime
from .models import Order, Order_item
from customers.models import CustomerAddress
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def query_orders(user_id):
    orders = Order.objects.filter(user_id=user_id)
    arr = []
    for order in orders:
        arr.append(order.ordersn)
    print arr
    return arr

def query_order_by_ordersn(ordersn):
    arr = []
    order_items = Order_item.objects.filter(ordersn=ordersn)
    for order_item in order_items:
        dic = []
        dic['product_id'] = order_item.product_id
        dic['price'] = order_item.price
        dic['amount'] = order_item.amount
        arr.append(dic)
    jsonStr = json.dumps(arr, ensure_ascii=False, encoding='UTF-8')
    print arr
    return jsonStr

def index(request):
    return render(request, 'orders/index.html')
@csrf_exempt
def make_order(request):
    if request.method == "GET":
        user_id = request.user.id;
        customerAddress = CustomerAddress.objects.filter(user_id=user_id)[0]
        add = {}
        add['name'] = customerAddress.name
        add['phone'] = customerAddress.phone
        add['address'] = customerAddress.address + " " + customerAddress.door_number
        return render(request, 'orders/make_order.html', {'add':add})
    if request.method == 'POST':
        jsonStr = json.loads(request.body)
        Arr = jsonStr
        print Arr
        ordersn = int(math.floor(time.mktime(timezone.now().timetuple()))) + random.randint(0, 1000)
        total_price = 0
        for i in Arr:
            item = Order_item()
            item.ordersn = ordersn
            item.product_id = i['id']
            item.price = i['price']
            item.amount = i['amount']
            item.save()
            total_price += item.price * item.amount
        order = Order()
        order.user_id = request.user.id
        order.ordersn = ordersn
        order.total_price = total_price
        delta = datetime.timedelta(minutes=30)  # 30分钟后过期
        order.exp_date = timezone.now() + delta
        order.save()
        result = {}
        result['code'] = 1
        res = json.dumps(result)
        print res.decode("unicode-escape")
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")


