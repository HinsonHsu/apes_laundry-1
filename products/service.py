# -*- coding: utf-8 -*-
from django.db import connections
from .models import Categories, Categories_cities, Products, Price_rules, Prices


def get_all_stations_by_city(city_id):
    cursor = connections['aliyun'].cursor()
    cursor.execute('select id, name from stations where city_id = %s', str(city_id))
    return dictfetchall(cursor)


def get_all_products():
    cursor = connections['aliyun'].cursor()
    cursor.execute('select id, name, logo from categories where is_del = 0')
    return dictfetchall(cursor)


def get_products_by_city(city_id):
    cursor = connections['aliyun'].cursor()
    cursor.execute(
        'select a.id,a.name,a.logo from categories as a, categories_cities as b where b.city_id = %s and a.id = b.category_id;',
        str(city_id))
    return dictfetchall(cursor)


def get_category_by_id(id):
    cursor = connections['aliyun'].cursor()
    cursor.execute('select id, name, logo from categories where id = %s' % str(id))
    return dictfetchall(cursor)


def check_category_and_city(category_id, city_id):
    category_city = Categories_cities.objects.filter(category_id=category_id, city_id=city_id)
    if len(category_city) == 0:
        return False
    else:
        return True


def get_products_by_id(id):
    cursor = connections['aliyun'].cursor()
    sql = 'select id, name, logo from products where category_id = %s and  is_del = 0' % str(id)
    cursor.execute(sql)
    return dictfetchall(cursor)


def add_price_to_products(products, city_id):
    grade = ['price1', 'price2', 'price3', 'price4', 'price5']
    for product in products:
        product_id = product['id']
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
            product['price'] = product_price
        except IndexError as e:
            price = Prices.objects.filter(product_id=product_id)[0]
            product['price'] = price.price1
    return products


def getCities():
    cursor = connections['aliyun'].cursor()
    cursor.execute('select id, name from cities')
    return dictfetchall(cursor)


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
        ]
