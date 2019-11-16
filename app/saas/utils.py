


from lib.utils.mytime import UtilTime
from lib.utils.exceptions import PubErrorCustom
import hashlib
from lib.utils.log import logger
from app.saas.config import *

def timeHandler(timeSpan,timeUnit):
    if timeUnit == 'y':
        return UtilTime().today.shift(years=timeSpan).timestamp
    elif timeUnit == 'm':
        return UtilTime().today.shift(months=timeSpan).timestamp
    elif timeUnit == 'd':
        return UtilTime().today.shift(days=timeSpan).timestamp
    elif timeUnit == 'h':
        return UtilTime().today.shift(hours=timeSpan).timestamp
    else:
        return timeUnit



def sortKeyStringForDict(data):
    s=""
    for item in sorted({k: v for k, v in data.items() if v != ""}):
        s+=data[item]
    return s

def sha256hex(data):
    sha = hashlib.sha256()
    sha.update(data.encode())
    return sha.hexdigest()

def sha1hex(data):
    sha = hashlib.sha1()
    sha.update(data.encode())
    return sha.hexdigest()

def passwordhash(password,salt):
    return sha1hex("{}-{}-{}".format(password,salt,AUTHKEY))

def signCheckForTx(signature, timestamp, eventId):

    if UtilTime().today.shift(seconds=-30).timestamp > int(timestamp):
        logger.info("请求timestamp已经超时!")
        raise PubErrorCustom("拒绝访问!")

    stringNew = sortKeyStringForDict(dict(
        token = TOKEN,
        timestamp=timestamp,
        eventId=eventId
    ))

    sign = sha256hex(stringNew)

    logger.info("{}----{}".format(signature, sign))
    # if signature != sign:
    #     logger.info("{}----{}".format(signature,sign))
    #     raise PubErrorCustom("签名错误!")

