import json
from Config import config
from slack import WebClient
from flask import Flask, request, jsonify
from Log import Log

class SlackBot:
    def __init__(self):
        self.slack_client = WebClient(token=config["Slack"]["BOT_TOKEN"])

    def work(self):
        app = Flask(__name__)

        @app.route("/", methods=["POST"])
        def web_hook():
            return self.handle_request(request.get_json(force=True))

        app.run(host=config["Flask"]["HOST"], port=config["Flask"]["PORT"])

    def handle_request(self, data):
        if data["type"] == "url_verification":
            return self.process_verification(data["token"], data["challenge"])
        elif data["event"]["type"] == "team_join":
            return self.process_team_join(data)
        elif data["event"]["type"] == "message" and "subtype" not in data["event"]:
            return self.process_reply_keyword(data)
        return "ok"

    def process_verification(self, token, challenge):
        if token == config["Slack"]["VERIFY_TOKEN"]:
            data = {
                "challenge": challenge
            }
            return jsonify(data)
        return None

    def process_team_join(self, data):
        if data["token"] == config["Slack"]["VERIFY_TOKEN"]:
            self.slack_client.chat_postMessage(channel=data["event"]["user"]["id"], text="欢迎加入wuhan2020项目：\n" \
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
        return "ok"

    def process_reply_keyword(self, data):
        channel = data["event"]["channel"]
        if channel in config["Bot"]["REPLY_CHANNEL"]:
            message = data["event"]["text"]
            if self.have_keyword(message, "TEAM_UI"):
                self.slack_client.chat_postMessage(channel=channel, text="<#CT70SHJQ0|team-designer>")
            elif self.have_keyword(message, "TEAM_API"):
                self.slack_client.chat_postMessage(channel=channel, text="<#CT72RFLEL|api-server-java> <#CT998PWDU|api-server-golang> <#CT3V5CDKJ|api-server>")
            elif self.have_keyword(message, "TEAM_FRONT_END"):
                self.slack_client.chat_postMessage(channel=channel, text="<#CT93L48H5|team-frontend>")
            elif self.have_keyword(message, "TEAM_DATA_SCIENCE"):
                self.slack_client.chat_postMessage(channel=channel, text="<#CT93L48H5|team-frontend>")
        return "ok"

    def have_keyword(self, text, key):
        for each in config["Bot"][key].split("$"):
            if each in text and "#" not in text:
                return True
        return False


SlackBot().work()
