from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def go_to_intro(self, event):
        return event.message.text.lower() == "人物介紹"


    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "go to state1"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def is_going_to_state3(self, event):
        text = event.message.text
        return text.lower() == "go to state3"

    

    def on_enter_begin(self, event):
        story="我們發現學藝股長的大秘密那天，是這樣開始的...\n\n輸入人物介紹查看角色"
        send_text_message(event.reply_token, story)

    def on_exit_begin(self):
        print('Leaving begin')

    def on_enter_intro(self, event):
        intro="1 => 班長\n2 => 學藝股長\n3 => 副班長\n4 => 體育股長\n5 => 風紀股長\ne => 離開"
        send_text_message(event.reply_token, intro)

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

    def on_enter_state3(self, event):
        print("I'm entering state3")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state3")
        self.go_back()

    def on_exit_state3(self):
        print("Leaving state3")
