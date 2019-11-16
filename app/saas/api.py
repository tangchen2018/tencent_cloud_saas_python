
import random

from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector
from lib.utils.exceptions import PubErrorCustom
import json
from app.saas.utils import signCheckForTx,timeHandler,passwordhash
from lib.utils.mytime import UtilTime

from app.saas.models import Saas,Users

from lib.utils.log import logger

class SaasAPIView(viewsets.ViewSet):

    @list_route(methods=['POST'])
    @Core_connector(transaction=True)
    def saasapi(self, request):

        logger.info("""
            request data: \n
             --- {} --- \n
             --- {} ---
        """.format(request.query_params,request.data))

        signCheckForTx(
            request.query_params.get("signature"),
            request.query_params.get("timestamp"),
            request.query_params.get("eventId"))

        #身份校验
        if request.data.get("action") == 'verifyInterface':
            return {"echoback":request.data.get("echoback")}
        #创建实例
        elif request.data.get("action") == 'createInstance':

            try:
                userObj = Users.objects.get(username = request.data.get("accountId"))
                isLoginFrist=True
                memo = "您的账号已存在，账号为{}，请使用应用信息中的免登地址一键授权登陆。免费体验版只能体验一次，如您希望再次免费体验请联系客服".format(userObj.username)
            except Users.DoesNotExist:
                isLoginFrist = False
                password = str(random.randint(10000000, 99999999))
                salt = str(random.randint(10000000, 99999999))
                ip="127.0.0.1"
                today = UtilTime().timestamp
                userObj = Users.objects.create(**dict(
                    username  = request.data.get("accountId"),
                    endtime = timeHandler(request.data.get("productInfo").get("timeSpan"),request.data.get("productInfo").get("timeUnit")),
                    password = passwordhash(password,salt),
                    salt = salt,
                    joinip = ip,
                    joindate = today,
                    lastip = ip,
                    lastvisit = today,
                    status=2,
                    type=1,
                    owner_uid=0,
                    groupid = 6
                ))

            saasObj = Saas.objects.create(**dict(
                orderId = request.data.get("orderId"),
                openId = request.data.get("openId"),
                productId =request.data.get("productId"),
                productInfo = json.dumps(request.data.get("productInfo")),
                uid = userObj.uid
            ))

            api_return={
                "signId": saasObj.signId,
                "appInfo":{
                    "website": "https://api.aihangge.com/",
                    "authUrl" : "https://api.aihangge.com/qcloud/callback.html"
                },
            }

            if not isLoginFrist:
                api_return["additionalInfo"]=[
                    {
                        "name": "官网地址",
                        "value": "https://www.aihangge.com"
                    },
                    {
                        "name": "登陆网址",
                        "value": "https://api.aihangge.com"
                    },
                    {
                        "name": "登陆账号",
                        "value": userObj.username
                    },
                    {
                        "name": "登陆密码",
                        "value": password
                    },
                    {
                        "name": "温馨提示",
                        "value": "如果您需要帮助请联系官网客服人员（电话：15176427685）同微信"
                    },
                ]
            else:
                api_return["additionalInfo"]=[
                    {
                        "name": "官网地址",
                        "value": "https://www.aihangge.com"
                    },
                    {
                        "name": "提醒说明",
                        "value": memo
                    },
                    {
                        "name": "登陆网址",
                        "value": "https://api.aihangge.com"
                    },
                    {
                        "name": "温馨提示",
                        "value": "如果您需要帮助请联系官网客服人员（电话：15176427685）同微信"
                    },
                ]

            saasObj.api_return=api_return
            saasObj.save()
            return api_return
        #实例续费通知接口
        elif request.data.get("action") == 'renewInstance':

            try:
                obj = Users.objects.get(username=request.data.get("accountId"))
            except Saas.DoesNotExist:
                logger.info("账号不存在! {}".format(request.data.get("accountId")))
                raise PubErrorCustom("账号不存在!")

            obj.endtime = UtilTime().string_to_timestamp(request.data.get("instanceExpireTime"))
            obj.save()
            return {"success":True}

        #实例配置变更通知接口
        elif request.data.get("action") == 'modifyInstance':
            try:
                saasObj = Saas.objects.get(signId=request.data.get("signId"))
            except Saas.DoesNotExist:
                logger.info("实例不存在! {}".format(request.data.get("signId")))
                raise PubErrorCustom("实例不存在!")

            try:
                obj = Users.objects.get(uid=saasObj.uid)
            except Saas.DoesNotExist:
                logger.info("账号不存在! {}".format(saasObj.uid))
                raise PubErrorCustom("账号不存在!")

            saasObj.productId = request.data.get("productId")
            saasObj.save()

            obj.endtime= timeHandler(request.data.get("timeSpan"),request.data.get("timeUnit"))
            obj.save()

            return {
                "success":True,
                "appInfo": {
                    "website": "https://api.aihangge.com/",
                    "authUrl": "https://api.aihangge.com/qcloud/callback.html"
                }
            }
        #实例过期通知接口
        elif request.data.get("action") == 'expireInstance':
            try:
                obj = Users.objects.get(username=request.data.get("accountId"))
            except Saas.DoesNotExist:
                logger.info("账号不存在! {}".format(request.data.get("accountId")))
                raise PubErrorCustom("账号不存在!")

            obj.endtime = UtilTime().today.replace(seconds=-1).timestamp
            obj.save()
            return {"success": True}
        #实例销毁通知接口
        elif request.data.get("action") == 'destroyInstance':
            return {"success": True}