import json
import os
import time
from colorama import Fore, Style
from dotenv import dotenv_values
import redis
from lolapy import LolaContext
from lolapy import Middleware
from lolapy import LolaSDK
from redis_lru import RedisLRU
from lolapy_notifications.caching.memory_cache import MemoryCache
from lolapy_notifications.notification_middleware import NotificationsMiddleware



class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class NotificationsManager(metaclass=Singleton):

    def __init__(self):
        print (f"{Fore.GREEN}NotificationsMiddlewareFactory created{Style.RESET_ALL}")

    def configure(self, 
                  redis_url, 
                  lola: LolaSDK, 
                  get_id=lambda x: x.get('lead', {}).get('signature'), 
                  key_prefix='lola:pn:',
                  store=None
        ):
        self.store = store or MemoryCache(key_prefix=key_prefix)
        self.middleware = NotificationsMiddleware(redis_url, lola, get_id, key_prefix, self.store)
        print (f"{Fore.GREEN}NotificationsMiddlewareFactory configured{Style.RESET_ALL}")
        return self.middleware

    def get_middleware(self):
        if not hasattr(self, 'middleware'):
            raise Exception('NotificationsMiddleware not configured')
        
        return self.middleware
