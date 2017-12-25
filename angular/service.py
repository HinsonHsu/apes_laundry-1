#! -*- coding: utf-8 -*-
from customers.models import Customer
from orders.models import Order, Order_item
from products.models import Products

import json, math, time, random, datetime
from customers.models import CustomerAddress

from django.utils import timezone




def getCompletedOrders(customer_id):
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


def getUnCompletedOrders(customer_id):
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


def isLogined(request):
    ua = request.META.get('HTTP_Authorization')
    if not ua:
        return False
    else:
        return True


def login_angular(request):
    from aliyun_msg.aliyun_msg import verify_phoneCode
    from users.models import User
    from customers.models import Customer, Customer_card
    USER_TYPE = 1  # 1 表示用户端
    USER_LABEL = "customer_"
    received_json_data = json.loads(request.body)
    phone = received_json_data.get("phone")
    username = USER_LABEL + phone
    code = received_json_data.get("checkCode")
    vc = verify_phoneCode(phone=phone, code=code, type=USER_TYPE)
    result = {}
    if vc == 1:
        try:
            user = User.objects.get(username=username);
            result["code"] = 0
            result['authorization'] = phone
        except User.DoesNotExist:
            # result["errMsg"] = "手机号未注册用户，用户不存在，请先注册！"
            # result["result"] = "fail"
            user = User(username=username);
            user.set_password(username)
            user.is_active = 1
            user.save()
            # 注册用户信息
            customer = Customer(name=username)
            customer.phone = phone
            customer.user_back_id = user.id
            customer.save()
            # 注册地用户会员卡
            customer_card = Customer_card()
            customer_card.customer_id = customer.id
            customer_card.real_money = 0
            customer_card.fake_money = 0
            customer_card.save()
            result["code"] = 0
            result['authorization'] = phone
    elif vc == 2:
        result["errMsg"] = "验证码过期，请重新发送验证码！"
        result["code"] = 2
    elif vc == 3:
        result["errMsg"] = "验证码错误，请输入正确的验证码！"
        result["code"] = 3
    elif vc == 4:
        result["errMsg"] = "请先发送验证！"
        result["code"] = 4
    return result
