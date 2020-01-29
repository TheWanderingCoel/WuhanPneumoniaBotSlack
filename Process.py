from Config import *
from flask import jsonify
from Log import Log
from Utils import *


class Process:

    def __init__(self):
        self.welcome_ts = "0"
        self.keyword_ts = "0"

    def process_verification(self, token, challenge):
        if token == config["Slack"]["VERIFY_TOKEN"]:
            data = {
                "challenge": challenge
            }
            return jsonify(data)
        return None

    def process_team_join(self, slack, data):
        if data["token"] == config["Slack"]["VERIFY_TOKEN"]:
            if config["Bot"]["WELCOME_REPLY_METHOD"] == "Private":
                if data["event"]["event_ts"] != self.welcome_ts:
                    resp = slack.chat_postMessage(channel="USTE69PUK", text="欢迎加入wuhan2020项目：\n" \
                                                                 "本项目核心是一个数据同步项目，把志愿者填写的石墨文档数据，同步到github上，然后方便各个端进行展示呈现。\n\n" \
                                                                 "===技能组===\n" \
                                                                 "<#CT70SHJQ0|team-designer> 设计技能组\n" \
                                                                 "<#CT99VDWS2|team-requirement-management> 产品需求管理技能组\n" \
                                                                 "<#CT93L48H5|team-frontend> 前端技能组\n" \
                                                                 "<#CT93MCEJK|team-backend> 后端技能组\n\n" \
                                                                 "其他技能组channel欢迎添加，命名格式：team-技能名称\n" \
                                                                 "===开发项目组===\n" \
                                                                 "<#CT4AV807P|proj-data-sync> 数据同步项目\n" \
                                                                 "<#CSTPXN533|proj-front-pages> web展示项目\n" \
                                                                 "<#CT6HW3X8E|proj-map-visualization> 数据地图可视化项目\n\n" \
                                                                 "其他项目组channel欢迎添加，命名格式：proj-项目名称")
                    Log.info("向 %s 用户发送了欢迎信息" % data["event"]["user"]["id"])
                    Log.debug(f"设置welcome_ts 为 f{self.welcome_ts}")
            elif config["Bot"]["WELCOME_REPLY_METHOD"] == "Public":
                slack.chat_postMessage(channel="USTE69PUK", text="123")
        return "ok"

    def process_reply_keyword(self, slack, data):
        Log.debug(data)
        channel = data["event"]["channel"]
        if channel in config["Bot"]["REPLY_CHANNEL"] and data["event"]["ts"] != self.keyword_ts:
            message = data["event"]["text"]
            if have_keyword(message, "TEAM_UI"):
                self.keyword_ts = data["event"]["ts"]
                slack.chat_postMessage(channel=channel, text="<#CT70SHJQ0|team-designer>")
            elif have_keyword(message, "TEAM_API"):
                self.keyword_ts = data["event"]["ts"]
                slack.chat_postMessage(channel=channel,
                                              text="<#CT72RFLEL|api-server-java> <#CT998PWDU|api-server-golang> <#CT3V5CDKJ|api-server>")
            elif have_keyword(message, "TEAM_FRONT_END"):
                self.keyword_ts = data["event"]["ts"]
                slack.chat_postMessage(channel=channel, text="<#CT93L48H5|team-frontend>")
            elif have_keyword(message, "TEAM_DATA_SCIENCE"):
                self.keyword_ts = data["event"]["ts"]
                slack.chat_postMessage(channel=channel, text="<#CT93L48H5|team-frontend>")
        return "ok"
