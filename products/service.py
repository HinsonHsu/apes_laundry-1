# -*- coding: utf-8 -*-
from django.db import connections

def get_all_products():
    cursor = connections['aliyun'].cursor()
    cursor.execute('select id, name, logo from categories where is_del = 0')
    return dictfetchall(cursor)

def get_category_by_id(id):
    cursor = connections['aliyun'].cursor()
    cursor.execute('select id, name, logo from categories where id = %s', str(id))
    return dictfetchall(cursor)

def get_products_by_id(id):
    cursor = connections['aliyun'].cursor()
    cursor.execute('select id, name, logo from products where category_id = %s and  is_del = 0',str(id))
    return dictfetchall(cursor)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]



