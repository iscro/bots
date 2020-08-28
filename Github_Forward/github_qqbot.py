#!/usr/bin/env python3

# 监听github事件，转发到qq群
# 项目依赖：https://github.com/bloomberg/python-github-webhook

from github_webhook import Webhook
from flask import Flask
import requests
import json

global qq
qq = 1919268092


def post(act, s_data):
    resp = requests.post(
        url="http://forwardmail:8000/{}".format(act), data=json.dumps(s_data))
    res = json.loads(resp.text)
    return res


def sendmsg(t_qq, s_msg):
    r = post("auth", {"authKey": "pass1234"})
    session = r['session']
    r = post("verify", {"sessionKey": session, "qq": qq})
    r = post("sendGroupMessage", {
        "sessionKey": session,
        "target": t_qq,
        "messageChain": [
            {"type": "Plain", "text": "{}".format(s_msg)},
        ]
    })
    r = post("release", {"sessionKey": session, "qq": qq})


app = Flask(__name__)  # Standard Flask app
webhook = Webhook(app)  # Defines '/postreceive' endpoint


@app.route("/")        # Standard Flask endpoint
def hello_world():
    return "Hello, World!"


@webhook.hook()        # Defines a handler for the 'push' event
def on_push(data):
    msg = "[GitHub]新push操作\n\n"
    msg += "Repo: {}\n\n".format(data["repository"]["full_name"])
    msg += "Pusher: {}\n\n".format(data["pusher"]["name"])
    msg += "Commit author: {}\n\n".format(data["commits"][0]["author"]["name"])
    msg += "说明: {}".format(data["commits"][0]["message"])
    if data["commits"][0]["added"]:
        msg += "\n\n添加的文件: {}".format(str(data["commits"][0]["added"]))
    if data["commits"][0]["removed"]:
        msg += "\n\n移除的文件: {}".format(str(data["commits"][0]["removed"]))
    if data["commits"][0]["modified"]:
        msg += "\n\n修改的文件: {}".format(str(data["commits"][0]["modified"]))
    if data["repository"]["private"] == False:
        msg += "\n\n点击 https://github.com/{} 查看详情".format(
            data["repository"]["full_name"])
    sendmsg("808712612", msg)
    sendmsg("1078060367", msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008)
