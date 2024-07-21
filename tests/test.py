from datetime import datetime, timedelta

initial_timestamp = datetime.now().isoformat()

def is_6_seconds_late(initial_timestamp):
    initial_time = datetime.fromisoformat(initial_timestamp)
    current_time = datetime.now()
    time_difference = current_time - initial_time
    return time_difference >= timedelta(seconds=6)

import time
time.sleep(8)
print(is_6_seconds_late(initial_timestamp))