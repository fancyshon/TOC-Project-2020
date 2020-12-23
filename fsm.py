from transitions.extensions import GraphMachine

from utils import send_text_message


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
