# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as userlogin, logout as userlogout
import json, datetime

from users.models import User
from aliyun_msg.aliyun_msg import send_phoneCode, verify_phoneCode
from .models import CustomerAddress, Customer, Coupon

from .models import Customer_card, Customer_card_log, Customer_card_charge_settings

# Create your views here.
USER_TYPE = 1  # 1 表示用户端
USER_LABEL = "customer_"


@login_required()
def index(request):
    # print request.user.username
    username = request.user.username
    phone = username[9:]
    c = Customer.objects.filter(user_back_id=request.user.id)[0]
    customer_id = c.id;
    customer_card = Customer_card.objects.filter(customer_id=customer_id)[0]
    #优惠券数量
    now = datetime.datetime.now()
    start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
    coupons = Coupon.objects.filter(customer_id=customer_id, valid_to__gt=start, used_at=None);
    print len(coupons)
    return render(request, 'customers/index.html',
                  {"user_phone": phone, 'totalMoney': customer_card.real_money + customer_card.fake_money, 'couponNum': len(coupons)})


@csrf_exempt
def code(request):
    if request.method == "POST":
        result = {}
        phone = request.POST.get("phone")
        print("customer_phone:"), phone
        ret = send_phoneCode(phone=phone, type=USER_TYPE)
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
        return render(request, 'customers/log.html')
    if request.method == "POST":
        result = {}
        phone = request.POST.get("phone")
        username = USER_LABEL + phone
        code = request.POST.get("code")
        vc = verify_phoneCode(phone=phone, code=code, type=USER_TYPE)
        if vc == 1:
            try:
                user = User.objects.get(username=username);
                userlogin(request, user)
                result["result"] = "success"
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
                customer_card = Customer_card()
                customer_card.customer_id = customer.id
                customer_card.real_money = 0
                customer_card.fake_money = 0
                customer_card.save()
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
        return render(request, 'customers/register.html')
    if request.method == "POST":
        result = {}
        phone = request.POST.get("phone")
        username = USER_LABEL + phone
        code = request.POST.get("code")
        vc = verify_phoneCode(phone=phone, code=code, type=USER_TYPE)
        if vc == 1:
            try:
                user = User.objects.get(username=username);
                userlogin(request, user)
                result["result"] = "success"
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
    return HttpResponseRedirect('/customers/login/')


@csrf_exempt
def test(request):
    return render(request, "customers/test.html")


@csrf_exempt
def address(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        door_number = request.POST.get('door_number')
        # sex = request.POST.get('sex')
        sex = True
        try:
            customer_address = CustomerAddress.objects.filter(user_id=request.user.id)[0]
            customer_address.name = name
            customer_address.phone = phone
            customer_address.door_number = door_number
            customer_address.sex = sex
            customer_address.save()
        except IndexError:
            customer_address = CustomerAddress(name=name, phone=phone, address=address, door_number=door_number,
                                               sex=sex)
            customer_address.user_id = request.user.id
            customer_address.save()

        return HttpResponseRedirect('/customer/index/')
    if request.method == "GET":
        user_id = request.user.id
        l = CustomerAddress.objects.filter(user_id=user_id)
        res = {}
        if len(l) > 0:
            cuAddress = l[0]
            res['result'] = "sucess"
            res['name'] = cuAddress.name
            res['phone'] = cuAddress.phone
            res['address'] = cuAddress.address
            res['door_number'] = cuAddress.door_number
        res = json.dumps(res)
        return render(request, 'customers/address.html', {"res": res})


@csrf_exempt
def customer_address(request):
    user_id = request.user.id
    cuAddress = CustomerAddress.objects.filter(user_id=user_id)[0]
    res = {}
    res['result'] = "sucess"
    res['name'] = cuAddress.name
    res['phone'] = cuAddress.phone
    res['address'] = cuAddress.address
    res['door_number'] = cuAddress.door_number
    res = json.dumps(res)
    print res.decode("unicode-escape")
    return HttpResponse(res.decode("unicode-escape"), content_type="application/json")


def my_login(request):
    # err_msg = {}
    # import datetime,random
    # today_str = datetime.date.today().strftime("%Y%m%d")
    # verify_code_img_path = "%s/%s" %(settings.VERIFICATION_CODE_IMGS_DIR,
    #                                  today_str)
    # if not os.path.isdir(verify_code_img_path):
    #     os.makedirs(verify_code_img_path,exist_ok=True)
    # print("session:",request.session.session_key)
    # #print("session:",request.META.items())
    # random_filename = "".join(random.sample(string.ascii_lowercase,4))
    # random_code = verify_code.gene_code(verify_code_img_path,random_filename)
    # cache.set(random_filename, random_code,30)
    #
    # if request.method == "POST":
    #
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     _verify_code = request.POST.get('verify_code')
    #     _verify_code_key  = request.POST.get('verify_code_key')
    #
    #     print("verify_code_key:",_verify_code_key)
    #     print("verify_code:",_verify_code)
    #     if cache.get(_verify_code_key) == _verify_code:
    #         print("code verification pass!")
    #
    #         user = authenticate(username=username,password=password)
    #         if user is not None:
    #             login(request,user)
    #             request.session.set_expiry(60*60)
    #             return HttpResponseRedirect(request.GET.get("next") if request.GET.get("next") else "/")
    #
    #         else:
    #             err_msg["error"] = 'Wrong username or password!'
    #
    #     else:
    #         err_msg['error'] = "验证码错误!"

    # return render(request,'login.html',{"filename":random_filename, "today_str":today_str, "error":err_msg})
    return render(request, 'customers/my_login.html')


def coupon(request):
    if request.method == 'GET':
        customer_id = Customer.objects.filter(user_back_id=request.user.id)[0].id
        unUseCouponList = []
        usedCouponList = []
        expiredCouponList = []
        try:
            coupons = Coupon.objects.filter(customer_id=customer_id)
            now = datetime.date.today()
            for i in coupons:
                cp = {}
                cp['id'] = i.id
                cp['start_time'] = i.valid_from.strftime("%Y-%m-%d %H:%M:%S")
                cp['end_time'] = i.valid_to.strftime("%Y-%m-%d %H:%M:%S")
                cp['customer_id'] = i.customer_id
                cp['face_value'] = i.discount
                cp['lump_sum'] = i.premise
                if now > i.valid_to:
                    expiredCouponList.append(cp)
                elif i.used_at == None:
                    unUseCouponList.append(cp)
                else:
                    usedCouponList.append(cp)
        except IndexError as e:
            print e
        res = {}
        res['unUseCouponList'] = unUseCouponList
        res['usedCouponList'] = usedCouponList
        res['expiredCouponList'] = expiredCouponList

        return render(request, 'coupon/coupon1.html', {'coupons': json.dumps(res)})


def recharge(request):
    if request.method == 'GET':

        cccss = Customer_card_charge_settings.objects.all();
        customer_card_charge_setting = []
        i = 0
        for cccs in cccss:
            temp = {}
            temp['id'] = i
            temp['min'] = cccs.min;
            temp['money_give'] = cccs.money_give;
            customer_card_charge_setting.append(temp);
        return render(request, 'coupon/recharge_card.html',
                      {'customer_card_charge_setting': customer_card_charge_setting,
                       'cccs': json.dumps(customer_card_charge_setting)})
    if request.method == 'POST':
        c = Customer.objects.filter(user_back_id=request.user.id)[0]
        customer_id = c.id;
        real_money = request.POST['real_money']
        fake_money = request.POST['fake_money']
        real_money = float(real_money)
        fake_money = float(fake_money)

        customer_card = Customer_card.objects.filter(customer_id=customer_id)[0]
        customer_card.real_money += real_money;
        customer_card.fake_money += fake_money;
        customer_card.save();
        customer_card_log = Customer_card_log();
        customer_card_log.kind = 3;
        customer_card_log.real_money = real_money;
        customer_card_log.fake_money = fake_money;
        customer_card_log.loggable_type = "Customer"
        customer_card_log.loggable_id = 3
        customer_card_log.user_card_id = customer_card.id
        customer_card_log.save();
        result = {}
        result['code'] = 0
        res = json.dumps(result)
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")

def certificate(request):
    if request.method == 'GET':
        return render(request, 'coupon/certificate.html')
    if request.method == 'POST':
        customer_id = Customer.objects.filter(user_back_id=request.user.id)[0].id
        cdkey = request.POST['cdkey']
        result = {}
        try:
            coupons = Coupon.objects.filter(id=cdkey, customer_id=None)[0];
            coupons.customer_id = customer_id
            coupons.is_active = 1
            coupons.save()

            result['code'] = 0
        except IndexError as e:
            result['code'] = 1
            result['errMsg'] = u'序列号有误，请重试!'
        res = json.dumps(result)
        return HttpResponse(res.decode("unicode-escape"), content_type="application/json")



