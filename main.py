import json
import nest_asyncio
from Config import *
from slack import WebClient
from flask import Flask, request, jsonify
from Log import Log
from Utils import *
from Process import Process

Process = Process()
class SlackBot:
    def __init__(self):
        nest_asyncio.apply()
        self.slack_client = WebClient(token=config["Slack"]["BOT_TOKEN"])

    def work(self):
        app = Flask(__name__)

        @app.route("/", methods=["POST"])
        def web_hook():
            return self.handle_request(request.get_json(force=True))

        app.run(host=config["Flask"]["HOST"], port=config["Flask"]["PORT"])

    def handle_request(self, data):
        # Handle Slack Url Verification
        if data["type"] == "url_verification":
            return Process.process_verification(data["token"], data["challenge"])
        # A new user have joined team
        elif data["event"]["type"] == "team_join":
            if is_enable("WELCOME_REPLY_ENABLE"):
                return Process.process_team_join(self.slack_client, data)
            else:
                return "ok"
        # Received a new message
        elif data["event"]["type"] == "message" and "subtype" not in data["event"]:
            return Process.process_reply_keyword(self.slack_client, data)
        return "ok"

SlackBot().work()
