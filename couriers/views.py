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

USER_TYPE = 2 # 2 表示取送端
USER_LABEL = "courier_"

@login_required(login_url="/courier/login/")
def index(request):
    # print request.user.username
    return render(request, 'couriers/index.html')


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
        code = request.POST.get("captcha")
        vc = verify_phoneCode(phone=phone, code=code, type=USER_TYPE)
        if vc == 1:
            try:
                username = "curier_" + phone
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
                username = USER_LABEL + phone
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
        vc = verify_phoneCode(phone=phone, code=code, type=1)
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
    return HttpResponseRedirect('/couriers/login/')

@csrf_exempt
def test(request):
    return render(request,'couriers/map.html')

class CurierForm(forms.Form):
    img1 = forms.FileField()
    img2 = forms.FileField()
@csrf_exempt
def upload(request):

    if request.method == 'POST':
        import os
        f = request.FILES.get('idcard')
        baseDir = os.path.dirname(os.path.abspath(__name__));
        jpgdir = os.path.join(baseDir, 'static', 'upload');

        filename = os.path.join(jpgdir, f.name);
        fobj = open(filename, 'wb');
        for chrunk in f.chunks():
            fobj.write(chrunk);
        fobj.close();
        return HttpResponse('upload ok')
    return render(request, 'couriers/test.html')
@csrf_exempt
def test(request):
    if request.method == "POST":
        uf = CurierForm(request.POST, request.FILES)
        if uf.is_valid():
            return HttpResponse('upload ok!')
    else:
        uf = CurierForm()
    return render_to_response('couriers/register.html', {'uf': uf})

@csrf_exempt
def map(request):
    return render(request, 'couriers/map.html')

