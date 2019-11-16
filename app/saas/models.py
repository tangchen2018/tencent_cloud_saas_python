
from django.db import models

from lib.utils.mytime import UtilTime

from app.idGenerator import idGenerator

class Saas(models.Model):

    id=models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    signId = models.CharField(max_length=17,default='',verbose_name="实例唯一ID")
    orderId = models.CharField(max_length=50,default="",verbose_name="订单ID")
    openId = models.CharField(max_length=50,default="",verbose_name="客户的标识")
    productId = models.IntegerField(default=0,verbose_name="云市场产品ID")
    requestId = models.CharField(max_length=50,default='',verbose_name="接口请求的ID")
    productInfo = models.TextField(default="",verbose_name="产品信息json")
    email = models.CharField(max_length=100,default="",verbose_name="邮箱")
    mobile = models.CharField(max_length=100,default="",verbose_name="手机号")
    api_return = models.CharField(max_length=255,default="",verbose_name="返回值")
    status = models.IntegerField(default=1,verbose_name="状态 0-待发货 1-已发货")
    dateline = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.dateline:
            self.dateline = UtilTime().timestamp
        if not self.signId:
            self.signId = idGenerator().ordercode()
        return super(Saas, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '实例表'
        verbose_name_plural = verbose_name
        db_table = 'ims_supermanx_qcloud'

class Users(models.Model):

    uid=models.AutoField(primary_key=True)
    owner_uid = models.IntegerField(default=0)

    groupid = models.IntegerField(default=0)
    founder_groupid = models.IntegerField(default=0)

    username = models.CharField(max_length=30,default='',verbose_name="用户名称")
    password = models.CharField(max_length=200,default='',verbose_name="密码")

    salt = models.CharField(max_length=10,default='',verbose_name="密码加密位")

    type = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    joindate = models.IntegerField(default=0)
    joinip = models.CharField(max_length=15,default='')
    lastvisit = models.IntegerField(default=0)
    lastip = models.CharField(max_length=15,default='')
    remark = models.CharField(max_length=500,default='')

    starttime = models.IntegerField(default=0)
    endtime = models.IntegerField(default=0)

    register_type = models.IntegerField(default=0)
    openid = models.CharField(max_length=50,default='')
    welcome_link = models.IntegerField(default=0)
    gid = models.IntegerField(default=0)
    notice_setting = models.CharField(max_length=5000,default='')
    is_bind = models.IntegerField(default=0)

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        db_table = 'ims_users'