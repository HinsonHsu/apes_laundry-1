#! -*- coding: utf-8 -*-
from customers.models import Customer
from orders.models import Order, Order_item
from products.models import Products

import json, math, time, random, datetime
from customers.models import CustomerAddress

from django.utils import timezone
CUSTOMER_ID = 6
def getCompletedOrders():
    customer_id = CUSTOMER_ID  # customer_18813090664
    orders = Order.objects.filter(customer_id=customer_id, status=4).order_by("-updated_at")
    orders_detail = []
    for order in orders:
        totalprice = 0
        order_items = Order_item.objects.filter(ordersn=order.ordersn)
        clothes_detail = {}
        clothes = []
        for order_item in order_items:
            cloth = {}
            cloth['id'] = order_item.product_id
            p = Products.objects.filter(id=order_item.product_id)[0]
            cloth['name'] = p.name
            cloth['price'] = order_item.price
            cloth['amount'] = order_item.amount
            cloth['logo'] = p.logo
            clothes.append(cloth)
            totalprice += cloth['price'] * cloth['amount']
        clothes_detail['ordersn'] = order.ordersn
        clothes_detail['name'] = order.customer_name
        clothes_detail['address'] = order.address
        clothes_detail['orderTime'] = order.created_at.strftime("%Y-%m-%d %H:%M:%S")
        clothes_detail['orderPrice'] = totalprice;
        clothes_detail['orderProducts'] = clothes
        orders_detail.append(clothes_detail)
    return orders_detail

def getUnCompletedOrders():
    customer_id = CUSTOMER_ID  # customer_18813090664
    orders = Order.objects.filter(customer_id=customer_id, status=1).order_by("-updated_at")
    orders_detail = []
    for order in orders:
        totalprice = 0
        order_items = Order_item.objects.filter(ordersn=order.ordersn)
        clothes_detail = {}
        clothes = []
        for order_item in order_items:
            cloth = {}
            cloth['id'] = order_item.product_id
            p = Products.objects.filter(id=order_item.product_id)[0]
            cloth['name'] = p.name
            cloth['price'] = order_item.price
            cloth['amount'] = order_item.amount
            cloth['logo'] = p.logo
            clothes.append(cloth)
            totalprice += cloth['price'] * cloth['amount']
        clothes_detail['ordersn'] = order.ordersn
        clothes_detail['name'] = order.customer_name
        clothes_detail['address'] = order.address
        clothes_detail['orderTime'] = order.created_at.strftime("%Y-%m-%d %H:%M:%S")
        clothes_detail['orderPrice'] = totalprice;
        clothes_detail['orderProducts'] = clothes
        orders_detail.append(clothes_detail)
    return orders_detail

def get_order_by_ordersn(ordersn):
    order = Order.objects.filter(ordersn=ordersn)[0]
    totalprice = 0
    order_items = Order_item.objects.filter(ordersn=order.ordersn)
    order_detail = {}
    clothes = []
    for order_item in order_items:
        cloth = {}
        cloth['id'] = order_item.product_id
        p = Products.objects.filter(id=order_item.product_id)[0]
        cloth['name'] = p.name
        cloth['price'] = order_item.price
        cloth['amount'] = order_item.amount
        cloth['logo'] = p.logo
        clothes.append(cloth)
        totalprice += cloth['price'] * cloth['amount']
    order_detail['ordersn'] = order.ordersn
    order_detail['name'] = order.customer_name
    order_detail['address'] = order.address
    order_detail['orderTime'] = order.created_at.strftime("%Y-%m-%d %H:%M:%S")
    order_detail['orderPrice'] = totalprice;
    order_detail['orderProducts'] = clothes
    return order_detail

def make_order(user_id, jsonStr):
    user_back_id = user_id
    customer_id = Customer.objects.filter(user_back_id=user_back_id)[0].id
    Arr = jsonStr
    ordersn = int(math.floor(time.mktime(timezone.now().timetuple()))) + random.randint(0, 1000)
    total_price = 0
    for i in range(len(Arr)):
        item = Order_item()
        item.ordersn = ordersn
        item.product_id = Arr[i]['id']
        item.price = Arr[i]['price']
        item.amount = Arr[i]['amount']
        item.save()
        total_price += item.price * item.amount
    city_id = 4
    order = Order()
    order.customer_id = customer_id
    order.ordersn = ordersn
    order.total_price = total_price
    order.city_id = city_id
    order.status = 1
    customer_address = CustomerAddress.objects.filter(user_id=user_back_id)[0]
    order.customer_name = customer_address.name
    order.phone = customer_address.phone
    order.address = customer_address.address + " " + customer_address.door_number
    delta = datetime.timedelta(minutes=30)  # 30分钟后过期
    order.exp_date = timezone.now() + delta
    order.save()
    result = {}
    result['code'] = 0
    return result;