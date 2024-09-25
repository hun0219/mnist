import pytz
from datetime import datetime

def now():
    now_time = datetime.now(pytz.timezone("Asia/Seoul"))
    rt = now_time.strftime('%Y-%m-%d %H:%M:%S')
    return rt
