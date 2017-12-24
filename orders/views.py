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
from customers.models import CustomerAddress, Customer, Coupon, Customer_card, Customer_card_log


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
        for state in range(1, 6):
            orders = Order.objects.filter(customer_id=customer_id, status=state).order_by("-updated_at")
            orders_detail = []
            i = 0
            for order in orders:
                order_items = Order_item.objects.filter(ordersn=order.ordersn)
                clothes_detail = {}
                clothes = []

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
        # 优惠券信息
        customer_id = Customer.objects.filter(user_back_id=request.user.id)[0].id
        unUseCouponList = []
        try:
            now = datetime.datetime.now()
            start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
            coupons = Coupon.objects.filter(customer_id=customer_id, valid_from__lt=start, used_at=None);
            for i in coupons:
                cp = {}
                cp['id'] = i.id
                cp['start_time'] = i.valid_from.strftime("%Y-%m-%d %H:%M:%S")
                cp['end_time'] = i.valid_to.strftime("%Y-%m-%d %H:%M:%S")
                cp['customer_id'] = i.customer_id
                cp['face_value'] = i.discount
                cp['lump_sum'] = i.premise
                unUseCouponList.append(cp)
        except IndexError as e:
            print e
        return render(request, 'orders/index.html',
                      {"orders": json.dumps(res), 'unUseCouponList': json.dumps(unUseCouponList)})


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
        return render(request, 'orders/make_order.html', {'add': add})
    if request.method == 'POST':
        customer_id = Customer.objects.filter(user_back_id=request.user.id)[0].id
        jsonStr = json.loads(request.body)
        Arr = jsonStr
        print Arr
        ordersn = int(math.floor(time.mktime(timezone.now().timetuple()))) + random.randint(0, 1000)
        total_price = 0
        # 数组前len(Arr) - 1元素为 order 信息
        for i in range(len(Arr) - 1):
            item = Order_item()
            item.ordersn = ordersn
            item.product_id = Arr[i]['id']
            item.price = Arr[i]['price']
            item.amount = Arr[i]['amount']
            item.save()
            total_price += item.price * item.amount
        # 数组最后一个元素为{"city_id": city_id}
        city_id = Arr[len(Arr) - 1]['city_id']
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
        customer_id = Customer.objects.filter(user_back_id=request.user.id)[0].id
        ordersn = request.POST['ordersn']
        coupon_id = int(request.POST['coupon_id'])
        print "coupon_id: {0}, ordersn: {1}".format(coupon_id, ordersn);
        order = Order.objects.filter(ordersn=ordersn)[0]
        minusPrice = 0;
        customer_card = Customer_card.objects.filter(customer_id=customer_id)[0]
        result = {}
        if coupon_id >= 0:
            coupon = Coupon.objects.get(id=coupon_id)
            minusPrice = coupon.discount;
        payPrice = order.total_price - minusPrice
        if customer_card.real_money + customer_card.fake_money >= payPrice:
            order.status = 4
            order.save()
            if customer_card.real_money >= payPrice:
                customer_card.real_money -= payPrice
                real_pay_money = -payPrice
                fake_pay_money = 0
            else:
                real_pay_money = -customer_card.real_money
                customer_card.fake_money += customer_card.real_money - payPrice
                fake_pay_money = payPrice - customer_card.real_money
                customer_card.real_money = 0
            customer_card.save();
            customer_card_log = Customer_card_log();
            customer_card_log.kind = 2;
            customer_card_log.real_money = real_pay_money;
            customer_card_log.fake_money = fake_pay_money;
            customer_card_log.loggable_type = "Customer"
            customer_card_log.loggable_id = 3
            customer_card_log.user_card_id = customer_card.id
            customer_card_log.save();
            # 计算是否使用了优惠券
            if coupon_id >= 0:
                coupon = Coupon.objects.get(id=coupon_id)
                coupon.used_at = datetime.date.today()
                coupon.save()
            result['code'] = 0
        else:
            result['code'] = 1
            result['errMsg'] = u'余额不足'
        res = json.dumps(result)
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")
