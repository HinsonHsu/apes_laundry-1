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
from products.models import Products
from customers.models import CustomerAddress, Customer
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
    if request.method == "GET":
        user_id = request.user.id
        customer_id = Customer.objects.filter(user_back_id=user_id)[0].id
        res = []
        for state in range(1,6):
            orders = Order.objects.filter(customer_id=customer_id, status=state).order_by("-updated_at")
            orders_detail = []
            i = 0
            for order in orders:
                order_items = Order_item.objects.filter(ordersn= order.ordersn)
                clothes_detail = {}
                clothes  = []

                for order_item in order_items:
                    cloth = {}
                    cloth['id'] = order_item.product_id
                    name = Products.objects.filter(id=order_item.product_id)[0].name
                    cloth['name'] = name
                    cloth['price'] = order_item.price
                    cloth['amount'] = order_item.amount
                    clothes.append(cloth)
                i += 1
                clothes_detail['id'] = i
                clothes_detail['order_ID'] = order.ordersn
                clothes_detail['name'] = order.customer_name
                clothes_detail['address_ID'] = order.address
                clothes_detail['order_time'] = order.created_at.strftime("%Y-%m-%d %H:%M:%S")
                clothes_detail['cloth'] = clothes
                orders_detail.append(clothes_detail)
            res.append(orders_detail)

        return render(request, 'orders/index.html', {"orders": json.dumps(res)})
@csrf_exempt
def make_order(request):
    if request.method == "GET":
        user_id = request.user.id;
        customerAddress = CustomerAddress.objects.filter(user_id=user_id)
        if len(customerAddress) > 0:
            customerAddress = customerAddress[0]
            add = {}
            add['name'] = customerAddress.name
            add['phone'] = customerAddress.phone
            add['address'] = customerAddress.address + " " + customerAddress.door_number
        else:
            add = None
        return render(request, 'orders/make_order.html', {'add':add})
    if request.method == 'POST':
        customer_id = Customer.objects.filter(user_back_id=request.user.id)[0].id
        jsonStr = json.loads(request.body)
        Arr = jsonStr
        print Arr
        ordersn = int(math.floor(time.mktime(timezone.now().timetuple()))) + random.randint(0, 1000)
        total_price = 0
        # 数组前len(Arr) - 1元素为 order 信息
        for i in range(len(Arr)-1):
            item = Order_item()
            item.ordersn = ordersn
            item.product_id = Arr[i]['id']
            item.price = Arr[i]['price']
            item.amount = Arr[i]['amount']
            item.save()
            total_price += item.price * item.amount
        #数组最后一个元素为{"city_id": city_id}
        city_id = Arr[len(Arr)-1]['city_id']
        order = Order()
        order.customer_id = customer_id
        order.ordersn = ordersn
        order.total_price = total_price
        order.city_id = city_id
        order.status = 1
        customer_address = CustomerAddress.objects.filter(user_id=request.user.id)[0]
        order.customer_name = customer_address.name
        order.phone = customer_address.phone
        order.address = customer_address.address + " " + customer_address.door_number
        delta = datetime.timedelta(minutes=30)  # 30分钟后过期
        order.exp_date = timezone.now() + delta
        order.save()
        result = {}
        result['code'] = 1
        res = json.dumps(result)
        print res.decode("unicode-escape")
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")
@csrf_exempt
def cancel_order(request):
    if request.method == "POST":
        ordersn = request.POST['ordersn']
        print "cancel:{0}".format(ordersn)
        order = Order.objects.filter(ordersn=ordersn)[0]
        order.status = 5
        order.save()
        result = {}
        result['code'] = 1
        res = json.dumps(result)
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")
@csrf_exempt
def pay_order(request):
    if request.method == "POST":
        ordersn = request.POST['ordersn']
        print "cancel:{0}".format(ordersn)
        order = Order.objects.filter(ordersn=ordersn)[0]
        order.status = 4
        order.save()
        result = {}
        result['code'] = 1
        res = json.dumps(result)
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")