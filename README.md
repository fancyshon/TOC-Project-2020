# TOC Project Line Bot互動式結局故事

作者:雷智翔
學號:F74076166

## Project內容

我認為FSM的特性很適合用來製作互動式的遊戲、故事等等，我想到我曾經在IG上看到的一個互動式故事，**#不再恐同**，透過點擊連結到不同帳號發展故事，而我將它改寫成LINE互動式聊天的版本，透過文字訊息達到相同的效果。

## 使用方式

- 首先先將這個Line帳號加入好友
    - ID : @084jgqqa
    - QR Code : 
        ![image](https://raw.githubusercontent.com/fancyshon/TOC_Project/master/img/qrcode.png)

- 加入好友後輸入`Start`(大小寫沒有差別)，聊天室便會開始指引你如何操作，基本上會有兩種輸入模式
    - 文字輸入
        機器人會提示你接下來要輸入什麼指令，如下圖
        ![image](https://raw.githubusercontent.com/fancyshon/TOC_Project/master/img/%E6%96%87%E5%AD%97%E8%BC%B8%E5%85%A5.png)

    - 按鈕輸入
        聊天室會產生一個按鈕的選單，上面是你目前有的選擇，根據你的想法選擇選項，如下圖
        ![image](https://raw.githubusercontent.com/fancyshon/TOC_Project/master/img/%E6%8C%89%E9%88%95.jpg)
    
- 依照你所做的選擇，故事最後會有3種結局。
- 其他指令
    - `show fsm`(大小寫沒有差別) 可得到當前的FSM結構圖
    - `重新開始` 可使整個故事從頭來過

## FSM Diagram

![image](https://tranquil-brook-42124.herokuapp.com/show-fsm)