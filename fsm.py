import os
from transitions.extensions import GraphMachine

from utils import send_text_message,send_image
from linebot import LineBotApi
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction,ImageSendMessage)

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    
    def on_enter_begin(self, event):
        reply_token = event.reply_token
        story="我們發現學藝股長的大秘密那天，是這樣開始的...\n\n--------------\n輸入 人物介紹 查看角色\n輸入 故事開始 開始這段故事\n你的所有選擇將會影響故事的走向"
        send_text_message(reply_token, story)

    def on_enter_intro(self, event):
        reply_token = event.reply_token
        intro="1 => 班長\n2 => 學藝股長\n3 => 副班長\n4 => 體育股長\n5 => 風紀股長\ne => 離開"
        send_text_message(reply_token, intro)

    def on_enter_1(self, event):
        reply_token = event.reply_token
        send_image(reply_token, "https://raw.githubusercontent.com/fancyshon/TOC_Project/master/img/%E7%8F%AD%E9%95%B7.png")
        self.back(event)

    def on_enter_2(self, event):
        reply_token = event.reply_token
        send_image(reply_token, "https://raw.githubusercontent.com/fancyshon/TOC_Project/master/img/%E5%AD%B8%E8%97%9D.png")
        self.back(event)

    def on_enter_3(self, event):
        reply_token = event.reply_token
        send_image(reply_token, "https://raw.githubusercontent.com/fancyshon/TOC_Project/master/img/%E5%89%AF%E7%8F%AD%E9%95%B7.png")
        self.back(event)

    def on_enter_4(self, event):
        reply_token = event.reply_token
        send_image(reply_token, "https://raw.githubusercontent.com/fancyshon/TOC_Project/master/img/%E9%AB%94%E8%82%B2.png")
        self.back(event)

    def on_enter_5(self, event):
        reply_token = event.reply_token
        send_image(reply_token, "https://raw.githubusercontent.com/fancyshon/TOC_Project/master/img/%E9%A2%A8%E7%B4%80.png")
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
                                text = '不想回答'
                            )
                        ]
                    )
            )
        )
    
    def on_enter_answer(self, event):
        reply_token = event.reply_token
        story = "學藝的手機被搶了過來，看著裡面的相簿裡滿滿的都是班長的照片，大家..."
        line_bot_api.reply_message(
            event.reply_token,[
            TemplateSendMessage(
                alt_text ='Buttons template',
                    template = ButtonsTemplate(
                        title = '你覺得...',
                        text = story,
                        actions=[
                            MessageTemplateAction(
                                label='哇，好尷尬...',
                                text = '哇，好尷尬...'
                            ),
                            MessageTemplateAction(
                                label='哈哈哈，我就知道!',
                                text = '哈哈哈，我就知道'
                            )
                        ]
                    )
            ),
            TextSendMessage(text="或者你想要阻止他們搶學藝手機\n輸入 阻止大家")
            ]
        )

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
                                text = '沒我的事'
                            ),
                            MessageTemplateAction(
                                label='看不下去',
                                text = '他們太誇張了，我會幫你想辦法處理的'
                            )
                        ]
                    )
            )
        )

    def on_enter_part3_2(self, event):
        reply_token = event.reply_token

        story="開朗的班長難得做出嫌惡的表情，學藝看起來快哭了。"
        line_bot_api.reply_message(
            event.reply_token, [
            TextSendMessage(text="有種的話，就和班長接吻啊!\n體育股長說。學藝漲紅著臉不說話"),
            TemplateSendMessage(
                alt_text ='Buttons template',
                    template = ButtonsTemplate(
                        title = '學藝會...',
                        text = story,
                        actions=[
                            MessageTemplateAction(
                                label='親臉頰就好了吧?',
                                text = '親臉頰就好了吧?'
                            ),
                            MessageTemplateAction(
                                label='喇機!喇機!(眾人在鼓譟)',
                                text = '喇機!喇機!(眾人在鼓譟)'
                            )
                        ]
                    )
            ),
            TextSendMessage(text="或是你覺得太過火了\n輸入 阻止大家")
            ]
        )

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
                                text = '別欺負他，住手拉!'
                            ),
                            MessageTemplateAction(
                                label='應該沒關係吧',
                                text = '他沒說甚麼，開玩笑應該沒關係吧'
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
                                label='聯絡他',
                                text = '跟他說:回來上課吧，我會幫你跟大家說清楚'
                            ),
                            MessageTemplateAction(
                                label='沒我的事',
                                text = '沒我的事'
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

    def on_enter_part4_1(self , event):
        reply_token = event.reply_token
        story = "來講現場一個人的祕密吧!\n副班長興沖沖的說。(我想聽學藝的，副班長接著說)"
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text ='Buttons template',
                    template = ButtonsTemplate(
                        title = '你覺得',
                        text = story,
                        actions=[
                            MessageTemplateAction(
                                label='其實我也有點好奇',
                                text = '其實我也有點好奇'
                            )
                        ]
                    )
            )
        )

    def on_enter_secret(self, event):
        reply_token = event.reply_token
        story = "其實...學藝他真的喜歡男生!!!\n班長說\n原來學藝是GAY大家..."
        line_bot_api.reply_message(
            event.reply_token,[
            TemplateSendMessage(
                alt_text ='Buttons template',
                    template = ButtonsTemplate(
                        title = '秘密',
                        text = story,
                        actions=[
                            MessageTemplateAction(
                                label='果然呢',
                                text = '果然呢'
                            ),
                            MessageTemplateAction(
                                label='早就覺得她很奇怪',
                                text = '早就覺得她很奇怪'
                            )
                        ]
                )
            ),
            TextSendMessage(text="這樣說人家秘密真的好嗎\n輸入 阻止班長")
            ]
        )

    def on_enter_part4_2(self, event):
        reply_token = event.reply_token
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text ='Buttons template',
                    template = ButtonsTemplate(
                        title = '大冒險',
                        text = '把書包打開給大家看看吧!不知道會不會又違禁品呢\n體育股長這樣要求。',
                        actions=[
                            MessageTemplateAction(
                                label='打開書包',
                                text = '打開書包'
                            )
                        ]
                    )
            )
        )

    def on_enter_open_bag(self, event):
        reply_token = event.reply_token
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text ='Buttons template',
                    template = ButtonsTemplate(
                        title = '班長將書包打開',
                        text = '一封情書掉了出來，竟然是學藝寫的\n你覺得',
                        actions=[
                            MessageTemplateAction(
                                label='哇!超讚的八卦',
                                text = '哇!超讚的八卦'
                            ),
                            MessageTemplateAction(
                                label='學藝應該很崩潰吧',
                                text = '學藝應該很崩潰吧'
                            )
                        ]
                    )
            )
        )

    #        send_text_message(reply_token, story)

    
    def on_enter_bad_ending(self, event):
        reply_token = event.reply_token
        story = "-----------------"
        line_bot_api.reply_message(
            event.reply_token, [
            TextSendMessage(text="幾個禮拜後，看這學藝空空的座位，沒想到因為這起事件導致他轉到別的學校，就這樣逼走自己的同學，我真的做對了嗎"),
            TemplateSendMessage(
                alt_text ='Buttons template',
                    template = ButtonsTemplate(
                        title = '怎麼會這樣',
                        text = story,
                        actions=[
                            MessageTemplateAction(
                                label='繼續',
                                text = '繼續'
                            )
                        ]
                    )
            )

            ]
        )
        
    def on_enter_good_ending(self, event):
        reply_token = event.reply_token
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text="很慶幸我當時有站出來幫他和大家對話，讓學藝知道他不是孤單一人，我覺得這才是朋友真正應該做的"),
                ImageSendMessage(original_content_url="https://raw.githubusercontent.com/fancyshon/TOC_Project/master/img/good_end.png", preview_image_url="https://raw.githubusercontent.com/fancyshon/TOC_Project/master/img/good_end.png"),
                TextSendMessage(text="故事結束")
            ]
        )

    def on_enter_suicide_ending(self, event):
        story = "-----------------"
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text="起初我們以為這只是個玩笑，直到導師告訴全班這個消息時候，我們才知道一點都不好笑，原來在經過班上幾個個禮拜不開其擾的霸凌後，學藝輕生了。"),
                ImageSendMessage(original_content_url="https://raw.githubusercontent.com/fancyshon/TOC_Project/master/img/dead_end.png",preview_image_url="https://raw.githubusercontent.com/fancyshon/TOC_Project/master/img/dead_end.png"),

                TemplateSendMessage(
                    alt_text ='Buttons template',
                        template = ButtonsTemplate(
                            title = '到底怎麼變成這樣的',
                            text = story,
                            actions=[
                                MessageTemplateAction(
                                    label='繼續',
                                    text = '繼續'
                                )
                            ]
                        )
                )
            ]
        )

    def on_enter_final_result(self, event):
        reply_token = event.reply_token
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text="回想之前的每個時刻，其實我們都有機會站出來為他發生，性向沒有對錯，錯的是你的觀念"),
                ImageSendMessage(original_content_url="https://raw.githubusercontent.com/fancyshon/TOC_Project/master/img/final.png", preview_image_url="https://raw.githubusercontent.com/fancyshon/TOC_Project/master/img/final.png"),
                TextSendMessage(text="故事結束")
            ]
        )
        