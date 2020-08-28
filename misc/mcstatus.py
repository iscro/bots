from mirai import Mirai, Plain, MessageChain, Group, Image
import asyncio
import urllib.request
import json


qq = 1919268092
authKey = 'pass1234'
mirai_api_http_locate = 'forwardmail:8000/ws'

app = Mirai(f"mirai://{mirai_api_http_locate}?authKey={authKey}&qq={qq}")


@app.receiver("GroupMessage")
async def event_gm(app: Mirai, message: MessageChain, group: Group):
    @app.exception_handler()
    async def exception_handler_normal(context):
        pass
    if message.toString() == "/mcstatus" or message.toString() == "/服务器状态":
        resp = urllib.request.urlopen(
            "http://iscrohlj1.qicp.vip:33333/api/status/CatServer")
        resp_dict = json.loads(resp.read().decode("utf-8"))
        server_name = "(虚假的)2b2t"
        server_status = resp_dict['status']
        server_online_players = resp_dict['current_players']
        await app.sendGroupMessage(group, [
            Plain(text="服务器：{}\n当前状态：{}\n在线人数：{}".format(
                server_name, server_status, server_online_players))
        ])
        return 0


if __name__ == "__main__":
    app.run()
