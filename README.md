# apes_laundry-1
Django 在线洗衣系统 mysql + 七牛云存储 + 阿里云短信服务

# 基本架构
mysql 系统数据库，采用Django orm 模型直接转换为mysql表

七牛云存储 图片采用七牛的云服务进行存储，进行静态图片分离服务器

阿里云短信服务器 注册需要用手机号进行验证码登陆

# 模块划分
aliyun_msg 阿里云短信<br/>
angular 二次封住接口供angular 4构建的客户端使用<br/>
apes_laundry 核心配置<br/>
couriers 快递人员相关<br/>
customer 洗衣用户相关<br/>
orders 订单相关<br/>
products 洗衣产品相关<br/>
qiniu_storage 七牛云配置以及上传<br/>
static 静态文件<br/>
