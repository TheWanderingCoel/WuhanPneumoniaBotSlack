from Config import config
import time
from croniter import croniter
from datetime import datetime, timedelta

def is_enable(key):
    return config["Bot"][key] == "True"

def have_keyword(text, key):
    for each in config["Bot"][key].split("$"):
        if each in text and "#" not in text:
            return True
    return False

# Round time down to the top of the previous minute
def roundDownTime(dt=None, dateDelta=timedelta(minutes=1)):
    roundTo = dateDelta.total_seconds()
    if dt == None : dt = datetime.now()
    seconds = (dt - dt.min).seconds
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return dt + timedelta(0,rounding-seconds,-dt.microsecond)

# Get next run time from now, based on schedule specified by cron string
def getNextCronRunTime(schedule):
    return croniter(schedule, datetime.now()).get_next(datetime)

# Sleep till the top of the next minute
def sleepTillTopOfNextMinute():
    t = datetime.utcnow()
    sleeptime = 60 - (t.second + t.microsecond/1000000.0)
    time.sleep(sleeptime)

def post_multi_channel(slack, channel_list, text):
    for each in channel_list.split(" "):
        resp = slack.chat_postMessage(channel=each, text=text)
        if is_enable("PIN_BROCAST"):
            slack.pins_add(channel=each, timestamp=resp["ts"])