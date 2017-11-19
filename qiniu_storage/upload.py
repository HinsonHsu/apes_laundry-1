# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import os

# 需要填写你的 Access Key 和 Secret Key
access_key = 'fBA-FqvAj-1LDqlSDOa4kWtjeTv5YwSnGkt6tyTn'
secret_key = 'JiYk2z7R64C9UHS3T_8Kp-04FHtiogKxlmelYFQ0'

# 默认static/upload
baseDir = os.path.dirname(os.path.abspath(__name__));
filedir = os.path.join(baseDir, 'static', 'upload');

class Qiniu_Client(object):
    def __init__(self):
        pass


def qiniu_upload(fileName):
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'ruby'
    # 上传到七牛后保存的文件名
    key = fileName;
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    localfile = os.path.join(filedir,key)
    ret, info = put_file(token, key, localfile)
    print(info)
    print ret['key'] == key
    print ret['hash'] == etag(localfile)
