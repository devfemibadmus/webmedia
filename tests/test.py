
from datetime import datetime, timedelta

last_time = (datetime.now() - timedelta(seconds=6)).isoformat()

print(last_time)
print(datetime.now())