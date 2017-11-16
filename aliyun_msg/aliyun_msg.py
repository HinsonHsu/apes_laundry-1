# -*- coding: utf-8 -*-
from django.utils import timezone
import random

from .models import PhoneCaptcha
from .aliyun import send_code
# 验证手机验证码
#
# 返回值：1.认证成功，2.验证码过期， 3.验证码错误， 4.手机未发送验证码
def verify_phoneCode(phone,type,code):
    print 'phone:{0}, type:{1}, code:{2}'.format(phone, type, code)
    try:
        phoneCode = PhoneCaptcha.objects.filter(phone=phone, type=type, is_sent=True).order_by("-create_date")[0]
        dif = timezone.now()-phoneCode.create_date
        if dif.seconds < 300:
            if phoneCode.code == code:
                print u"认证成功"
                return 1  # 认证成功
            else:
                return 3  # 验证码错误
        else:
            return 2 #验证码过期

    except IndexError: #未查询到结果
        return 4 #手机未发送验证码

# 随机生成4位验证码
def generate_verifcation_code():
    code_list = []
    for i in range(10):
        code_list.append(str(i))
    myslice = random.sample(code_list, 4)
    verifcation_code = ''.join(myslice)
    return verifcation_code

def send_phoneCode(phone, type):
    """

    :param phone: 手机号
    :param type: 1.表示用户端， 2.表示取送端
    :return: ret: 返回结果字典，成功：{'code': 'OK', 'errMsg: '错误信息', 'phoneCode: '1234'}
                                失败：{'code': 'NO', 'errMsg: '错误信息'}
    """
    ret = {}
    try:
        phoneCaptcha = PhoneCaptcha.objects.filter(phone=phone, type=type).order_by("-create_date")[0]
        dif = timezone.now() - phoneCaptcha.create_date
        if dif.seconds < 300:
            ret['code'] = 'NO'
            ret['errMsg'] = u'您于5分钟内已发送验证码，请稍后再试！'
            return ret
    except IndexError:#未查询到结果
        pass
    random_code = generate_verifcation_code()
    try:
        phoneCaptcha = PhoneCaptcha(phone=phone, code=random_code, type=type)
        phoneCaptcha.save()
        res = send_code(phone=phoneCaptcha.phone, code=phoneCaptcha.code)
        res = eval(res) #str转为dict
        print res
        if res["Code"] == "OK":
            phoneCaptcha.is_sent = True
            phoneCaptcha.save()
            ret['code'] = 'OK'
            ret['phoneCode'] = phoneCaptcha.code
            return ret
        else:
            ret['code'] = 'NO'
            ret['errMsg'] = u'发送失败，请稍后再试！'
            return ret
    except:
        ret['code'] = 'NO'
        ret['errMsg'] = u'发送失败，请稍后再试！'
        return ret



