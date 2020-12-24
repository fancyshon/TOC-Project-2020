import os
from transitions.extensions import GraphMachine

from utils import send_text_message
from linebot import LineBotApi
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction)

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    
    def on_enter_begin(self, event):
        reply_token = event.reply_token
        story="我們發現學藝股長的大秘密那天，是這樣開始的...\n\n--------------\n輸入 人物介紹 查看角色\n輸入 故事開始 開始故事"
        send_text_message(reply_token, story)

    def on_enter_intro(self, event):
        reply_token = event.reply_token
        intro="1 => 班長\n2 => 學藝股長\n3 => 副班長\n4 => 體育股長\n5 => 風紀股長\ne => 離開"
        send_text_message(reply_token, intro)

    def on_enter_1(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "班長:他人緣很好，大家都聽他的")
        self.back(event)

    def on_enter_2(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "學藝股長:比女人還像女人，大家都懷疑他喜歡男生")
        self.back(event)

    def on_enter_3(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "副班長:總是附和班長")
        self.back(event)

    def on_enter_4(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "體育股長:最愛瞎鬧，有他在的地方都很熱鬧")
        self.back(event)

    def on_enter_5(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "風紀股長:負責管班上秩序，其實自己也很愛鬧")
        self.back(event)

    def on_enter_part1(self, event):
        reply_token = event.reply_token
        choice="\n\n-----------\n桌上有一個瓶子\n你想 1 => 順時針轉 ,2 => 逆時鐘轉"
        send_text_message(reply_token, "那天下午，在風紀的提議下，我們開始玩真心話大冒險"+choice)

    #順時鐘
    def on_enter_part2_1(self, event):
        reply_token = event.reply_token
        choice="\n\n-----------\n你選擇 1 => 真心話 ,2 => 大冒險"
        send_text_message(reply_token, "瓶子轉到學藝，大家開始鼓譟要他..."+choice)

    def on_enter_part3_1(self, event):
        reply_token = event.reply_token
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text ='Buttons template',
                    template = ButtonsTemplate(
                        title = '真心話',
                        text = '欸，老實說你是不是喜歡男生\n副班長問。',
                        actions=[
                            MessageTemplateAction(
                                label='不想回答',
                                text = '回答大家'
                            )
                        ]
                    )
            )
        )
    def on_enter_answer(self, event):
        reply_token = event.reply_token
        story = "學藝的手機被搶了過來，看著裡面的相簿裡滿滿的都是班長的照片，大家覺得..."
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text ='Buttons template',
                    template = ButtonsTemplate(
                        title = '你覺得...',
                        text = story,
                        actions=[
                            MessageTemplateAction(
                                label='哇，好尷尬...',
                                text = 'os'
                            ),
                            MessageTemplateAction(
                                label='哈哈哈，我就知道!',
                                text = 'laugh'
                            )
                        ]
                    )
            )
        )
        send_text_message(reply_token, "或者你想要阻止他們搶學藝手機\n輸入 阻止大家")

    def on_enter_embarassed(self, event):
        self.equal(event)
        
    def on_enter_bully(self, event):
        reply_token = event.reply_token
        story = "那天之後，這件事也在全班傳開了，死GAY，也成為學藝的名字，書桌上常常被寫一些不堪入目的字句。"
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text ='Buttons template',
                    template = ButtonsTemplate(
                        title = '你覺得',
                        text = story,
                        actions=[
                            MessageTemplateAction(
                                label='沒我的事',
                                text = 'nothing'
                            ),
                            MessageTemplateAction(
                                label='他們太誇張了，我會想辦法處理的',
                                text = 'help'
                            )
                        ]
                    )
            )
        )

    def on_enter_part3_2(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "有種的話，就和班長接吻啊!\n體育股長說。學藝漲紅著臉不說話")

        story="開朗的班長難得做出嫌惡的表情，學藝愾起來快哭了。"
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text ='Buttons template',
                    template = ButtonsTemplate(
                        title = '學藝會...',
                        text = story,
                        actions=[
                            MessageTemplateAction(
                                label='親臉頰就好了吧?',
                                text = 'cheek'
                            ),
                            MessageTemplateAction(
                                label='喇機!喇機!(眾人在鼓譟)',
                                text = 'french'
                            )
                        ]
                    )
            )
        )
        send_text_message(reply_token, "或是你覺得太過火了\n輸入 阻止大家")

    def on_enter_cheek_kiss(self, event):
        reply_token = event.reply_token
        story = "那天之後，大家更常對學藝開玩笑，看她沒什麼反應，我們也不以為意"
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text ='Buttons template',
                    template = ButtonsTemplate(
                        title = '你覺得',
                        text = story,
                        actions=[
                            MessageTemplateAction(
                                label='別欺負他，住手拉!',
                                text = 'concern'
                            ),
                            MessageTemplateAction(
                                label='他沒說甚麼，開他玩笑應該沒關係吧',
                                text = 'kidding'
                            )
                        ]
                    )
            )
        )

    def on_enter_french_kiss(self, event):
        reply_token = event.reply_token
        story = "那天之後，學藝跟班長變得很尷尬，也不太敢跟大家互動，越來越常缺席..."
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text ='Buttons template',
                    template = ButtonsTemplate(
                        title = '你覺得',
                        text = story,
                        actions=[
                            MessageTemplateAction(
                                label='跟他說:回來上課吧，我會幫你跟大家說清楚的。',
                                text = 'concern'
                            ),
                            MessageTemplateAction(
                                label='沒我的事',
                                text = 'nothing'
                            )
                        ]
                    )
            )
        )

    #逆時鐘
    def on_enter_part2_2(self, event):
        reply_token = event.reply_token
        choice="\n\n-----------\n你選擇 1 => 真心話 ,2 => 大冒險"
        send_text_message(reply_token, "瓶子轉到班長，大家開始鼓譟要他..."+choice)

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state1")
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "go to state1"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def is_going_to_state3(self, event):
        text = event.message.text
        return text.lower() == "go to state3"
