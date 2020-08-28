import email
import imaplib
import time,json,sys
import requests

qq = 1919268092
authKey = 'pass1234'
def sendmsg(s_msg):
    #第一个
    r=send("auth",{"authKey": "pass1234"})
    session=r['session']
    #print(r)
    r=send("verify",{"sessionKey": session,"qq": qq})
    #print(r)
    r=send("sendGroupMessage",{
        "sessionKey": session,
        "target": 1079073862,
        "messageChain": [
        { "type": "Plain", "text":"新邮件: {} ".format(s_msg) },
        #{ "type": "At", "target": 3534337252, "display": "@ALL"},
        #{ "type": "At", "target": 212576335, "display": "@ALL"},
        #{ "type": "At", "target": 2529728544, "display": "@ALL"},
        #{ "type": "At", "target": 254350165, "display": "@ALL"},
        #{ "type": "At", "target": 2258801611, "display": "@ALL"},
        #{ "type": "At", "target": 2552719904, "display": "@ALL"},
        #{ "type": "At", "target": 2281714638, "display": "@ALL"},
        #{ "type": "At", "target": 1925928574, "display": "@ALL"},
        #{ "type": "At", "target": 446786650, "display": "@ALL"},
        #{ "type": "At", "target": 3436175283, "display": "@ALL"},
        #{ "type": "At", "target": 377608133, "display": "@ALL"},
        #{ "type": "At", "target": 2789810433, "display": "@ALL"},
        #{ "type": "At", "target": 3221667468, "display": "@ALL"}
    ]
    })
    r=send("sendGroupMessage",{
        "sessionKey": session,
        "target": 1079073862,
        "messageChain": [
        { "type": "Plain", "text":"访问http://39.101.221.199/mail/latest.php查看邮件"},
    ]
    })
    print(r)
    r=send("release",{"sessionKey": session,"qq": qq})
    print(r)
    #第二个
    r=send("auth",{"authKey": "pass1234"})
    session=r['session']
    #print(r)
    r=send("verify",{"sessionKey": session,"qq": qq})
    #print(r)
    r=send("sendGroupMessage",{
        "sessionKey": session,
        "target": 1078060367,
        "messageChain": [
        { "type": "Plain", "text":"新邮件: {} ".format(s_msg) },
        #{ "type": "At", "target": 3534337252, "display": "@ALL"},
        #{ "type": "At", "target": 212576335, "display": "@ALL"},
        #{ "type": "At", "target": 2529728544, "display": "@ALL"},
        #{ "type": "At", "target": 254350165, "display": "@ALL"},
        #{ "type": "At", "target": 2258801611, "display": "@ALL"},
        #{ "type": "At", "target": 2552719904, "display": "@ALL"},
        #{ "type": "At", "target": 2281714638, "display": "@ALL"},
        #{ "type": "At", "target": 1925928574, "display": "@ALL"},
        #{ "type": "At", "target": 446786650, "display": "@ALL"},
        #{ "type": "At", "target": 3436175283, "display": "@ALL"},
        #{ "type": "At", "target": 377608133, "display": "@ALL"},
        #{ "type": "At", "target": 2789810433, "display": "@ALL"},
        #{ "type": "At", "target": 3221667468, "display": "@ALL"}
    ]
    })
    r=send("sendGroupMessage",{
        "sessionKey": session,
        "target": 1078060367,
        "messageChain": [
        { "type": "Plain", "text":"访问http://39.101.221.199/mail/latest.php查看邮件"},
    ]
    })
    print(r)
    r=send("release",{"sessionKey": session,"qq": qq})
    print(r)
def send(act,s_data):
    resp = requests.post(url="http://forwardmail:8000/{}".format(act),data=json.dumps(s_data))
    res=json.loads(resp.text)
    return res

def parseBody(message):
    global msg_text
    """ 解析邮件/信体 """
    # 循环信件中的每一个mime的数据块
    for part in message.walk():
        # 这里要判断是否是multipart，是的话，里面的数据是一个message 列表
        if not part.is_multipart():
            name = part.get_param("name")
            if name:
                pass
            else:
                msg_text=part.get_payload(decode=True)
                #print(msg_text)
                #msg_text = msg_text.replace(" ",",")
                msg_text = msg_text.replace("%","percent")
                msg_text = msg_text.replace("<","《")
                msg_text = msg_text.replace(">","》")
                with open("/mail/latest.txt",'w') as f:
                    f.write(msg_text.replace("script","br"))
def initialize_mail():
    global conn
    conn=imaplib.IMAP4_SSL(host="imap.qiye.aliyun.com",port=993)
    conn.login("secure-support@iscro.cn","ISCRO-Secure-Support233")


def check_new_mail():
    global subdecode
    global issent
    conn.select()
    type,data = conn.search(None, 'UNSEEN')
    maillist=data[0].split()
    #print(maillist)
    if len(maillist)==0:
        issent=False
        return 0
    type,data = conn.fetch(maillist[-1], '(RFC822)')
    msg = email.message_from_string(data[0][1].decode('utf-8'))
    #print(msg)
    subdecode = email.header.make_header(email.header.decode_header(msg['SUBJECT']))
    parseBody(msg)
    print("New mail: {}".format(subdecode))
    if issent==False:
        sendmsg(subdecode)
        issent=True
    conn.store(maillist[-1],'+FLAGS','\\SEEN')
    conn.logout()
    
print("Started IMAP service.")
#sendmsg('test')
#sendmsg('testok')
while True:
    try:
        initialize_mail()
        check_new_mail()
        time.sleep(5)
    except KeyboardInterrupt:
        sys.exit()
    except:
       pass
