# -*- coding: utf-8 -*-
from .models import Order, Order_item
from products.models import Products, Categories, Price_rules, Prices
import json


def get_unaccepted_order():
    # 未接单信息
    orders = Order.objects.filter(status=1)
    orders_detail = []
    i = 0
    totalprice = 0
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
            totalprice += cloth['price'] * cloth['amount']
        i += 1
        clothes_detail['id'] = i
        clothes_detail['orderId'] = order.ordersn
        clothes_detail['name'] = order.customer_name
        clothes_detail['address'] = order.address
        clothes_detail['time'] = order.created_at.strftime("%Y-%m-%d %H:%I:%S")
        clothes_detail['cloth'] = clothes
        clothes_detail['price'] = totalprice
        orders_detail.append(clothes_detail)
    return json.dumps(orders_detail)


def get_accepted_order_by_courier_id(courier_id):
    # 已接单信息
    orders = Order.objects.filter(status=2, courier_id=courier_id)
    orders_detail = []
    i = 0
    totalprice = 0
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
            totalprice += cloth['price'] * cloth['amount']
        i += 1
        clothes_detail['id'] = i
        clothes_detail['orderId'] = order.ordersn
        clothes_detail['name'] = order.customer_name
        clothes_detail['address'] = order.address
        clothes_detail['time'] = order.created_at.strftime("%Y-%m-%d %H:%I:%S")
        clothes_detail['cloth'] = clothes
        clothes_detail['price'] = totalprice
        orders_detail.append(clothes_detail)
    return json.dumps(orders_detail)


def get_complete_order_by_courier_id(courier_id):
    # 已完成信息
    orders = Order.objects.filter(status=4, courier_id=courier_id)
    orders_detail = []
    i = 0
    totalprice = 0
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
            totalprice += cloth['price'] * cloth['amount']
        i += 1
        clothes_detail['id'] = i
        clothes_detail['orderId'] = order.ordersn
        clothes_detail['name'] = order.customer_name
        clothes_detail['address'] = order.address
        clothes_detail['time'] = order.created_at.strftime("%Y-%m-%d %H:%I:%S")
        clothes_detail['cloth'] = clothes
        clothes_detail['price'] = totalprice
        orders_detail.append(clothes_detail)
    return json.dumps(orders_detail)
def get_order_by_ordersn(ordersn):
    order = Order.objects.filter(ordersn=ordersn)[0]
    city_id = order.city_id
    order_items = Order_item.objects.filter(ordersn=order.ordersn)
    totalprice = 0
    order_detail = {}
    clothes = []
    for order_item in order_items:
        cloth = {}
        cloth['id'] = order_item.product_id
        category_id = Products.objects.filter(id=order_item.product_id)[0].category_id
        category_products = []
        products = Products.objects.filter(category_id=category_id, is_del=0)
        for product in products:
            product_detail = {}
            product_detail['product_id'] = product.id
            product_detail['name'] = product.name
            product_id = product.id
            try:
                category_id = Products.objects.get(id=product_id).category_id
                grade_id = Price_rules.objects.filter(city_id=city_id, category_id=category_id).order_by("-from_date")[
                    0].grade
                price = Prices.objects.filter(product_id=product_id)[0]
                if grade_id == 1:
                    product_price = price.price1
                elif grade_id == 2:
                    product_price = price.price2
                elif grade_id == 3:
                    product_price = price.price3
                elif grade_id == 4:
                    product_price = price.price4
                elif grade_id == 5:
                    product_price = price.price5
                product_detail['price'] = product_price
            except IndexError as e:
                price = Prices.objects.filter(product_id=product_id)[0]
                product_detail['price'] = price.price1
            product_detail['name'] = product_detail['name'] + " " + str(product_detail['price'])
            category_products.append(product_detail)
        cloth["category_products"] = category_products
        name = Products.objects.filter(id=order_item.product_id)[0].name
        cloth['name'] = name
        cloth['price'] = order_item.price
        cloth['amount'] = order_item.amount
        cloth['name'] = cloth['name'] + " " + str(float(cloth['price']))
        clothes.append(cloth)
        totalprice += cloth['price'] * cloth['amount']
    order_detail['orderId'] = order.ordersn
    order_detail['name'] = order.customer_name
    order_detail['phone'] = order.phone
    order_detail['address'] = order.address
    order_detail['time'] = order.created_at.strftime("%Y-%m-%d %H:%I:%S")
    order_detail['cloth'] = clothes
    order_detail['price'] = totalprice

    order_msg = {}
    order_msg["orderId"] = order_detail["orderId"]
    order_msg['name'] = order_detail['name']
    order_msg['phone'] = order_detail['phone']
    order_msg['address'] = order_detail['address']
    return json.dumps(order_detail), order_msg