import json
import os
from datetime import datetime, timedelta
from typing import Tuple



LOG_FILE = 'usage_log.json'

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        json.dump({}, f)

def _load_log():
    with open(LOG_FILE, 'r') as f:
        return json.load(f)
    
def _save_log(log):
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)

def get_user_id(request):
    # fallback to IP - you can later add cookie or session support
    return request.client.host

def can_run_analysis(user_id: str, crawl: bool = False) -> Tuple[bool, str]:
    now = datetime.utcnow()
    today = now.strftime('%Y-%m-%d')
    log = _load_log()
    user = log.get(user_id, {})

    if crawl:
        last_crawl = user.get('last_crawl')
        if last_crawl and datetime.fromisoformat(last_crawl) > now - timedelta(days=7):
            return False, "You can only crawl 1 site per week on the free plan."
        return True, ''
    else:
        usage = user.get('usage', {})
        count = usage.get(today, 0)
        if count >= 5:
            return False, 'You have reached the free daily limit of 5 SEO checks.'
        return True, f'{5 - count - 1} checks remaining today.'
    
def record_analysis(user_id: str, crawl: bool = False):
    now = datetime.utcnow()
    today = now.strftime('%Y-%m-%d')
    log = _load_log()

    if user_id not in log:
        log[user_id] = {'usage': {}}

    if crawl:
        log[user_id]['last_crawl'] = now.isoformat()
    else:
        usage = log[user_id].get('usage', {})
        usage[today] = usage.get(today, 0) + 1
        log[user_id]['usage'] = usage

    _save_log(log)