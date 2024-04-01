import json
import time
from colorama import Fore, Style
import redis
from lolapy import LolaContext
from lolapy import Middleware
from lolapy import LolaSDK

from lolapy_notifications.caching.memory_cache import MemoryCache


class NotificationsMiddleware(Middleware):

    def __init__(self, 
                 redis_url, 
                 lola: LolaSDK, get_id=lambda x: x.get('lead', {}).get('signature'), 
                 key_prefix='lola:pn:',
                 store=None
        ):
        print (f"{Fore.GREEN}NotificationsMiddleware created{Style.RESET_ALL}")

        self.name = 'NotificationsMiddleware'
        self.get_id = get_id
        self.redis_client = redis.from_url(redis_url)
        self.lola = lola
        self.store = store or MemoryCache(key_prefix=key_prefix)


    def process_request(self, session, ctx: LolaContext, req):
        # TODO: implement register self.register(session['lead']['metadata']['phone'], session)
        id = self.get_id(req)
        print (f"{Fore.GREEN}{self.name}: Processing ID: {id}{Style.RESET_ALL}")
        self.touch(id, session)
        


    def get_context(self, session):
        return self.lola.context(session)

    def touch(self, user_id, session):
        data = {
            'session': session,
            'last_update': int(round(time.time() * 1000))
        }
        self.store.set(user_id, data)
        print(f'{Fore.GREEN}{self.name}: Touched user_id for push notifications: {user_id}{Style.RESET_ALL}')

    def get(self, user_id):
        data = self.store.get(user_id)
        if data:
            return json.loads(data)
        return None

    def delete_entry(self, user_id):
        self.store.delete(user_id)

    def search_user_by_id(self, user_id):
        try:
            return self.store.get(user_id)
        except KeyError:
            return None        
        
    
    def get_all(self):
        return self.store.all()
    
    def push(self, user_id, message):

        # with green color
        print(f"{Fore.GREEN}{self.name}: Pushing notification to user_id: {user_id} -> message: {message}{Style.RESET_ALL}")

        client = self

        data = client.get(user_id)
        if data:
            session = data['session']
            ctx = client.get_context(session)

            last_update = data['last_update'] or 0

            print(f"{Fore.GREEN}{self.name}: Last update was less than 24 hrs ago. Last enroll update: {last_update}{Style.RESET_ALL}")

            # send message using lola messanger
            ctx.messanger.send_text_message(message, blend=True, appendToHistory=True)

            return True
        else:
            print(f"{Fore.RED}{self.name}: User not found in Notifications registry. User ID: {user_id}{Style.RESET_ALL}")

        
        return False





if __name__ == "__main__":

    pass
