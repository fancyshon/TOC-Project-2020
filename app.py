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
    "french_kiss", "cheek_kiss", "do_nothin", "concern_about",
    "answer", "embarassed", "bully",
    "secret","open_bag","love_letter"
    "good_ending","bad_ending","suicide_ending",
     "state1", "state2"],
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
            "trigger": "ans", "source": "truth", "dest": "answer",
        },
        {
            "trigger": "os", "source": "answer", "dest": "embarassed",
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
            "trigger": "drop", "source": "open_bag", "dest": "love_letter",
        },
        {
            "trigger": "gossip", "source": "love_letter", "dest": "bully",
        },
        {
            "trigger": "be_sympathy", "source": "love_letter", "dest": "cheek",
        },
        
        {"trigger": "go_back", "source": ["state1", "state2"], "dest": "user"},
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

now_state = "user"
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
        global now_state
        if event.message.text.lower() == "show fsm":
            send_image(event.reply_token ,"https://tranquil-brook-42124.herokuapp.com/show-fsm")
        else:
            if event.message.text.lower() == "start":
                now_state="start"
                machine.start(event)
            elif event.message.text == "人物介紹":
                now_state="intro"
                machine.introduction(event)

            if now_state == "intro":
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
                elif event.message.text == "e":
                    machine.fin_intro(event)
                    now_state = "start"
            elif now_state == "start":
                if event.message.text == "故事開始":
                    machine.go_to_part1(event)
                    now_state = "part1"
            elif now_state == "part1":
                if event.message.text == '1':
                    machine.go_to_part2_1(event)
                elif event.message.text == '2':
                    machine.go_to_part2_2(event)


            if now_state == "user":
                print("Fail")
                response = machine.advance(event)

            if response == False:
                send_text_message(event.reply_token, "Not Entering any State")
            print(now_state)

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
