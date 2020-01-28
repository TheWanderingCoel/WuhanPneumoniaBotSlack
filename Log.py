import time
from Config import *


class Loggger:

    def __init__(self, filename):
        self.filename = filename
        self.level = {
            "debug": 0,
            "info": 1,
            "warning": 2,
            "error": 3,
            "critical": 4
        }
        self.current_level = "raffle"
        # 统计日志行数
        self.count = 0

    def debug(self, data, level=0):
        data = f"{self.timestamp()} - DEBUG: {data}"
        print("\033[34;1m" + data + "\033[0m")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(data + "\n")

    def info(self, data, level=1):
        data = f"{self.timestamp()} - INFO: {data}"
        print("\033[32;1m" + data + "\033[0m")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(data + "\n")

    def warning(self, data, level=2):
        data = f"{self.timestamp()} - WARNING: {data}"
        print("\033[33;1m" + data + "\033[0m")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(data + "\n")

    def error(self, data, level=3):
        data = f"{self.timestamp()} - ERROR: {data}"
        print("\033[31;1m" + data + "\033[0m")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(data + "\n")

    def critical(self, data, level=4):
        data = f"{self.timestamp()} - CRITICAL: {data}"
        print("\033[36;1m" + data + "\033[0m")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(data + "\n")

    def timestamp(self):
        str_time = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
        return str_time


Log = Loggger(sys.path[0] + "/Log/Bot.log")
