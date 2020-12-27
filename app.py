import os
import sys
import pygraphviz as p

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message,send_image

load_dotenv()


machine = TocMachine(
    states=["user", "intro", "begin",
    "1", "2", "3", "4", "5",
    "part1", "part2_1", "part2_2", "part3_1", "part3_2", "part4_1", "part4_2",
    "french_kiss", "cheek_kiss",
    "answer", "embarassed", "bully",
    "secret","open_bag",
    "good_ending", "bad_ending", "suicide_ending",
    "final_result"
    ],
    transitions=[
        {
            "trigger": "introduction", "source": "begin", "dest": "intro",
        },
        {
            "trigger": "start", "source": "user", "dest": "begin",
        },
        {
            "trigger": "go1", "source": "intro", "dest": "1"
        },
        {
            "trigger": "go2", "source": "intro", "dest": "2"
        },
        {
            "trigger": "go3", "source": "intro", "dest": "3"
        },
        {
            "trigger": "go4", "source": "intro", "dest": "4"
        },
        {
            "trigger": "go5", "source": "intro", "dest": "5"
        },
        {
            "trigger": "back", "source": ["1", "2", "3", "4", "5"], "dest": "intro"
        },
        {
            "trigger": "fin_intro", "source": "intro", "dest": "begin",
        },
        {
            "trigger": "go_to_part1", "source": "begin", "dest": "part1",
        },
        #學藝真心話大冒險
        {
            "trigger": "go_to_part2_1", "source": "part1", "dest": "part2_1",
        },
        {
            "trigger": "truth", "source": "part2_1", "dest": "part3_1",
        },
        {
            "trigger": "ans", "source": "part3_1", "dest": "answer",
        },
        {
            "trigger": "os", "source": "answer", "dest": "embarassed",
        },
        {
            "trigger": "stop", "source": "answer", "dest": "good_ending",
        },
        {
            "trigger": "laugh_at", "source": "answer", "dest": "bully",
        },
        {
            "trigger": "nothing", "source": "bully", "dest": "suicide_ending",
        },
        {
            "trigger": "concern", "source": "bully", "dest": "good_ending",
        },
        {
            "trigger": "equal", "source": "embarassed", "dest": "cheek_kiss",
        },
        {
            "trigger": "dare", "source": "part2_1", "dest": "part3_2",
        },
        {
            "trigger": "stop", "source": "part3_2", "dest": "good_ending",
        },
        {
            "trigger": "french_kiss", "source": "part3_2", "dest": "french_kiss",
        },
        {
            "trigger": "nothing", "source": "french_kiss", "dest": "bad_ending",
        },
        {
            "trigger": "concern", "source": "french_kiss", "dest": "good_ending",
        },
        {
            "trigger": "kiss", "source": "part3_2", "dest": "cheek_kiss",
        },
        {
            "trigger": "kidding", "source": "cheek_kiss", "dest": "bad_ending",
        },
        {
            "trigger": "concern", "source": "cheek_kiss", "dest": "good_ending",
        },
        #班長真心話大冒險
        {
            "trigger": "go_to_part2_2", "source": "part1", "dest": "part2_2",
        },
        {
            "trigger": "truth", "source": "part2_2", "dest": "part4_1",
        },
        {
            "trigger": "tell_secret", "source": "part4_1", "dest": "secret",
        },
        {
            "trigger": "stop", "source": "secret", "dest": "good_ending",
        },
        {
            "trigger": "stop", "source": "secret", "dest": "good_ending",
        },
        {
            "trigger": "murmur", "source": "secret", "dest": "cheek_kiss",
        },
        {
            "trigger": "laugh", "source": "secret", "dest": "bully",
        },
        {
            "trigger": "dare", "source": "part2_2", "dest": "part4_2",
        },
        {
            "trigger": "open", "source": "part4_2", "dest": "open_bag",
        },
       {
            "trigger": "gossip", "source": "open_bag", "dest": "bully",
        },
        {
            "trigger": "be_sympathy", "source": "open_bag", "dest": "cheek_kiss",
        },
        {
            "trigger": "end", "source": ["bad_ending","suicide_ending"], "dest": "final_result",        
        }   
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)
app = Flask(__name__, static_url_path="")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")

        response = True
        if event.message.text.lower() == "show fsm":
            send_image(event.reply_token, "https://tranquil-brook-42124.herokuapp.com/show-fsm")

        else:
            if event.message.text == "重新開始":
                machine.state = "begin"
                send_text_message(event.reply_token,"已重新開始\n\n我們發現學藝股長的大秘密那天，是這樣開始的...\n\n--------------\n輸入 人物介紹 查看角色\n輸入 故事開始 開始這段故事\n你的所有選擇將會影響故事的走向")
            if event.message.text.lower() == "start":
                machine.start(event)
            elif event.message.text == "人物介紹":
                machine.introduction(event)

            if machine.state == "intro":
                if event.message.text == "1":
                    machine.go1(event)
                elif event.message.text == "2":
                    machine.go2(event)
                elif event.message.text == "3":
                    machine.go3(event)
                elif event.message.text == "4":
                    machine.go4(event)
                elif event.message.text == "5":
                    machine.go5(event)
                elif event.message.text == "離開":
                    machine.fin_intro(event)
            elif machine.state == "begin":
                if event.message.text == "故事開始":
                    machine.go_to_part1(event)
            elif machine.state == "part1":
                if event.message.text == '1':
                    machine.go_to_part2_1(event)
                elif event.message.text == '2':
                    machine.go_to_part2_2(event)
            elif machine.state == "part2_1":
                if event.message.text == '1':
                    machine.truth(event)
                elif event.message.text == '2':
                    machine.dare(event)
            elif machine.state == "part3_1":
                if event.message.text == "不想回答":
                    machine.ans(event)
            elif machine.state =="answer":
                if event.message.text == "哇，好尷尬...":
                    machine.os(event)
                elif event.message.text == "哈哈哈，我就知道":
                    machine.laugh_at(event)
                elif event.message.text == "阻止大家":
                    machine.stop(event)
            elif machine.state == "bully":
                if event.message.text == "沒我的事":
                    machine.nothing(event)
                elif event.message.text == "他們太誇張了，我會幫你想辦法處理的":
                    machine.concern(event)
            elif machine.state == "part3_2":
                if event.message.text == "親臉頰就好了吧?":
                    machine.kiss(event)
                elif event.message.text == "喇機!喇機!(眾人在鼓譟)":
                    machine.french_kiss(event)
                elif event.message.text =="阻止大家":
                    machine.stop(event)
            elif machine.state == "cheek_kiss":
                if event.message.text == "他沒說甚麼，開玩笑應該沒關係吧":
                    machine.kidding(event)
                elif event.message.text == "別欺負他，住手拉!":
                    machine.concern(event)
            elif machine.state == "french_kiss":
                if event.message.text == "跟他說:回來上課吧，我會幫你跟大家說清楚":
                    machine.concern(event)
                elif event.message.text == "沒我的事":
                    machine.nothing(event)
            elif machine.state == "part2_2":
                if event.message.text == '1':
                    machine.truth(event)
                elif event.message.text == '2':
                    machine.dare(event)
            elif machine.state == "part4_1":
                if event.message.text == "其實我也有點好奇":
                    machine.tell_secret(event)
            elif machine.state == "secret":
                if event.message.text == "果然呢":
                    machine.murmur(event)
                elif event.message.text == '早就覺得她很奇怪':
                    machine.laugh(event)
                elif event.message.text == "阻止班長":
                    machine.stop(event)
            elif machine.state == "part4_2":
                if event.message.text == "打開書包":
                    machine.open(event)
            elif machine.state == "open_bag":
                if event.message.text == "哇!超讚的八卦":
                    machine.gossip(event)
                elif event.message.text == "學藝應該很崩潰吧":
                    machine.be_sympathy(event)
            elif machine.state == "suicide_ending" or machine.state == "bad_ending":
                if event.message.text == "繼續":
                    machine.end(event)

            if response == False :
                send_text_message(event.reply_token, "Not Entering any State")
            print(machine.state)

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
