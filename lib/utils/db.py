
import json
from   django_redis  import   get_redis_connection
from lib.utils.exceptions import PubErrorCustom
from lib.utils.mytime import UtilTime

class RedisHandler(object):
    def __init__(self,**kwargs):
        self.redis_client = get_redis_connection(kwargs.get("db") if kwargs.get("db") else 'default')
        self.key = str(kwargs.get("key"))

    def redis_dict_set(self,value):
        self.redis_client.set(self.key,json.dumps(value))

    def redis_dict_get(self):
        res = self.redis_client.get(self.key)
        return json.loads(res) if res else res

class RedisIdGenerator(RedisHandler):

    def __init__(self,**kwargs):
        kwargs.setdefault('db','generator')
        if not kwargs.get("key",None):
            raise PubErrorCustom("key不能为空!")
        super().__init__(**kwargs)

    def run(self):
        raise PubErrorCustom("Not is func!")

class RedisIdGeneratorForUser(RedisIdGenerator):
    """
    获取用户ID,通过传入角色ID获取值
    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def run(self):
        return "%s%06d"%(self.key,self.redis_client.incr(self.key))

class RedisIdGeneratorForOrder(RedisIdGenerator):
    """
    获取订单ID
    """
    def __init__(self,**kwargs):
        t = UtilTime().arrow_to_string(format_v="YYYYMMDDHHmmss")
        kwargs.setdefault('key', t)
        super().__init__(**kwargs)

    def run(self):
        res = "%s%03d"%(self.key,self.redis_client.incr(self.key))
        self.redis_client.expire(self.key,10)
        return res

class RedisCaCheHandlerBase(RedisHandler):

    def __init__(self,**kwargs):
        kwargs.setdefault('db', 'cache')
        if not kwargs.get("key",None):
            raise PubErrorCustom("key不能为空!")

        super().__init__(**kwargs)

    def redis_dict_set(self,dictKey,value):
        self.redis_client.hset(self.key,dictKey,json.dumps(value))

    def redis_dict_get(self,dictKey):
        res = self.redis_client.hget(self.key,dictKey)
        return json.loads(res) if res else res

    def redis_dict_del(self,dictKey):
        self.redis_client.hdel(self.key,dictKey)
        return None

    def redis_dict_delall(self):
        self.redis_client.delete(self.key)
        return None

    def redis_dict_get_all(self):

        res = self.redis_client.hgetall(self.key)
        res_ex={}
        if res:
            for key in res:
                res_ex[key.decode()] = json.loads(res[key])
        return res_ex if res else None

class RedisTokenHandler(RedisHandler):
    def __init__(self,**kwargs):
        kwargs.setdefault('db', 'token')
        super().__init__(**kwargs)