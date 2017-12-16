# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as userlogin, logout as userlogout
from django.contrib.auth.decorators import login_required

from users.models import User
from aliyun_msg.aliyun_msg import send_phoneCode, verify_phoneCode
from qiniu_storage.service import writeFile
from login_required import login_required_courier
from orders.service import get_unaccepted_order, get_accepted_order_by_courier_id, get_complete_order_by_courier_id, get_order_by_ordersn
from .models import Courier
from orders.models import  Order, Order_item
USER_TYPE = 2 # 2 表示取送端
USER_LABEL = "courier_"

@login_required_courier()
def index(request):
    # print request.user.username
    return render(request, 'couriers/personal.html')


@csrf_exempt
def code(request):
    if request.method == "POST":
        result = {}
        phone = request.POST.get("phone")
        print("courier_phone:"), phone
        ret = send_phoneCode(phone=phone, type=USER_TYPE)# 2 表示取送端
        if ret['code'] == 'OK':
            result["result"] = "success"  # 1成功
            result["code"] = ret['code']
        else:
            result["result"] = "fail"  # 1成功
            result["errMsg"] = ret['errMsg']
        print "res:{0}".format(result)
        res = json.dumps(result)
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")


@csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request, 'couriers/login.html')
    if request.method == "POST":
        result = {}
        phone = request.POST.get("phone")
        code = request.POST.get("code")
        vc = verify_phoneCode(phone=phone, code=code, type=USER_TYPE)
        if vc == 1:
            try:
                username = "courier_" + phone
                user = User.objects.get(username=username);
                userlogin(request,user)
                result["result"] = "success"
            except User.DoesNotExist:
                # result["errMsg"] = "手机号未注册用户，用户不存在，请先注册！"
                # result["result"] = "fail"
                user = User(username=username);
                user.set_password(username)
                user.is_active = 1
                user.save()
                userlogin(request, user)
                result["result"] = "success"
        elif vc == 2:
            result["errMsg"] = "验证码过期，请重新发送验证码！"
            result["result"] = "fail"
        elif vc == 3:
            result["errMsg"] = "验证码错误，请输入正确的验证码！"
            result["result"] = "fail"
        elif vc == 4:
            result["errMsg"] = "请先发送验证！"
            result["result"] = "fail"
        res = json.dumps(result)
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")


@csrf_exempt
def register(request):
    if request.method == "GET":
        return render(request, 'couriers/register.html')
    if request.method == "POST":
        result = {}
        phone = request.POST.get("phone")
        username = USER_LABEL + phone
        code = request.POST.get("code")
        vc = verify_phoneCode(phone=phone, code=code, type=2)
        if vc == 1:
            try:
                user = User.objects.get(username=username);
                userlogin(request,user)
                result["result"] = "success"
            except User.DoesNotExist:
                # result["errMsg"] = "手机号未注册用户，用户不存在，请先注册！"
                # result["result"] = "fail"
                user = User(username=username);
                user.set_password(username)
                user.is_active = 1
                user.save()
                from models import Courier
                courier = Courier()
                courier.phone = phone
                courier.user_back_id = user.id
                courier.save()
                userlogin(request, user)
                result["result"] = "success"
        elif vc == 2:
            result["errMsg"] = "验证码过期，请重新发送验证码！"
            result["result"] = "fail"
        elif vc == 3:
            result["errMsg"] = "验证码错误，请输入正确的验证码！"
            result["result"] = "fail"
        elif vc == 4:
            result["errMsg"] = "请先发送验证！"
            result["result"] = "fail"
        res = json.dumps(result)
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")


@csrf_exempt
def logout(request):
    userlogout(request)
    return HttpResponseRedirect('/courier/login/')


class CurierForm(forms.Form):
    img1 = forms.FileField()
    img2 = forms.FileField()
@csrf_exempt
# @login_required_courier()
def upload(request):
    from couriers.models import Courier
    if request.method == 'POST':
        user = request.user;
        name = request.POST.get('name')
        phone = user.username.split(USER_LABEL)[1]
        address = request.POST.get('address')
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')

        f1 = request.FILES.get('idcard')
        f2 = request.FILES.get('health')
        f1_name = writeFile(f1)
        f2_name = writeFile(f2)
        new_courier = Courier(name=name, phone=phone, workplace=address, idcard_url=f1_name, health_url= f2_name, latitude=latitude, longitude=longitude)
        new_courier.user_back_id = user.id
        new_courier.save()
        return HttpResponse('upload ok')
    return render(request, 'couriers/upload.html')

@csrf_exempt
@login_required_courier()
def notAccepted_orders(request):
    if request.method == "GET":
        orders = get_unaccepted_order()
        return render(request, 'couriers/notAccept.html', {'orders': orders})
    if request.method == "POST":
        ordersn = request.POST['ordersn']
        user_id = request.user.id
        c = Courier.objects.filter(user_back_id=user_id)[0]
        order = Order.objects.filter(ordersn=ordersn)[0]
        order.status = 2
        order.courier_id = c.id
        order.courier_name = c.name
        order.save()
        result = {}
        result['code'] = 1
        res = json.dumps(result)
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")
@login_required_courier()
def accepted_orders(request):
    c = Courier.objects.filter(user_back_id=request.user.id)[0]
    orders = get_accepted_order_by_courier_id(c.id)
    return render(request, 'couriers/accepted.html', {'orders': orders})
@login_required_courier()
def complete_orders(request):
    c = Courier.objects.filter(user_back_id=request.user.id)[0]
    orders = get_complete_order_by_courier_id(c.id)
    return render(request, 'couriers/completed.html', {'orders': orders})
@login_required_courier()
def personal(request):
    # print request.user.username
    return render(request, 'couriers/personal.html')
@csrf_exempt
@login_required_courier()
def orderDetail(request):
    if request.method == "GET":
        ordersn =  request.GET['ordersn']
        ord = Order.objects.filter(ordersn=ordersn)[0]
        order, order_msg = get_order_by_ordersn(ordersn)
        from products.service import get_all_stations_by_city
        stations = get_all_stations_by_city(city_id=ord.city_id)
        stationList = []
        for i in stations:
            stationList.append(i['name'])
        return render(request, 'couriers/orderDetail.html', {"order": order, 'order_msg': order_msg, 'stationList':stationList})
    if request.method == "POST":
        jsonStr = json.loads(request.body)
        print jsonStr
        ordersn = jsonStr['ordersn']
        target_station_index = jsonStr['station']
        order_items = jsonStr['order_items']
        order = Order.objects.filter(ordersn=ordersn)[0]
        from products.service import get_all_stations_by_city
        stations = get_all_stations_by_city(city_id=order.city_id)
        order.target_station_id = stations[target_station_index]['id']
        curOrder_items = Order_item.objects.filter(ordersn=ordersn)
        total_price = 0
        for i, order_item in enumerate(order_items):
            after_order_item = Order_item.objects.get(id=curOrder_items[i].id)
            print after_order_item.id
            after_order_item.product_id = order_item['id']
            after_order_item.name = order_item['name']
            after_order_item.price = order_item['price']
            after_order_item.amount = order_item['amount']
            after_order_item.save()
            total_price += curOrder_items[i].price * curOrder_items[i].amount
        order.total_price = total_price
        order.status = 3
        order.save()
        result = {}
        result['code'] = 1
        res = json.dumps(result)
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")