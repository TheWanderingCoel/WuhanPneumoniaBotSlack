from Config import config
from Utils import *

class BroadCast:
    def __init__(self, slack):
        self.method == config["Bot"]["BROADCAST_METHOD"]
        self.point = config["Bot"]["BROADCAST_POINT"]
        self.interval = config["Bot"]["BROADCAST_INTERVAL"]
        self.channel = config["Bot"]["BROADCAST_CHANNEL"]
        self.text = config["Bot"]["BROADCAST_TEXT"]
        self.slack = slack

    def work(self, slack):
        if not is_enable(""):
            return
        if self.method == "Point":
            self.work_point()
        elif self.method == "Interval":
            self.work_interval()

    def work_point(self):
        nextRunTime = getNextCronRunTime(self.point)
        while True:
            roundedDownTime = roundDownTime()
            if roundedDownTime == nextRunTime:
                post_multi_channel(self.slack, self.channel, self.text)
                nextRunTime = getNextCronRunTime(self.point)
            elif roundedDownTime > nextRunTime:
                # We missed an execution. Error. Re initialize.
                nextRunTime = getNextCronRunTime(self.point)
            sleepTillTopOfNextMinute()

    def work_interval(self):
        while True:
            post_multi_channel(self.slack, self.channel, self.text)
            time.sleep(int(self.interval) * 60)