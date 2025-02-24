import streamlit as st
import requests
import os

# 设置页面布局，并默认折叠侧边栏
st.set_page_config(page_title="深圳记忆", layout="wide", initial_sidebar_state="collapsed")

# 使用 CSS 隐藏 Streamlit 菜单、页脚和标题栏
st.markdown(
    """
    <style>
        /* 隐藏 Streamlit 右上角菜单 */
        #MainMenu {visibility: hidden;}
        
        /* 隐藏 Streamlit 页脚 */
        footer {visibility: hidden;}
        
        /* 隐藏 Streamlit 默认标题栏 */
        header {visibility: hidden;}
        
        /* 调整页面内容，使其更居中 */
        .block-container {
            padding-top: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* 标题居中 */
        .title {
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }

        /* 让生成的诗歌竖向显示 */
        .poem-column {
            writing-mode: vertical-rl;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: black;
            background-color: white;
            padding: 10px;
            display: inline-block;
        }

        /* 最右侧的第一列变红 */
        .poem-column.first {
            color: red;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# **创建左侧 Tab 选择**
tab = st.sidebar.radio("选择页面", ["深圳记忆", "下载历史"])

# **历史记录文件路径**
HISTORY_FILE = "history.txt"

# ================== 📌 **Tab 1: 深圳记忆** ==================
if tab == "深圳记忆":
    st.markdown("<div class='title'>深圳记忆</div>", unsafe_allow_html=True)

    # 用户输入框
    user_input = st.text_area("", placeholder="请输入一段记忆...", key="memory_input")

    # 让提交按钮居中
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit = st.button("提交")

    # 读取 API Key（从 Streamlit secrets 读取）
    API_KEY = st.secrets["api"]["key"]
    API_URL = "https://api2.aigcbest.top/v1/chat/completions"

    # 触发生成
    if submit:
        if not user_input.strip():
            st.warning("请输入内容后再提交！")
        else:
            # 生成 Prompt
            prompt = f"""
            **用户输入**：{user_input}

            解析用户输入的记忆片段，并生成极简风格的诗歌。风格要求：
            - **极简主义**：短句、克制的表达、避免冗余。
            - **画面感**：以具体意象呈现情绪，而非直接表达情感。
            - **留白**：让读者自行解读诗歌背后的故事和情绪。
            - **忠于用户输入**：不额外添加复杂修辞或过多形容词。
       解析用户输入的记忆片段，并生成极简风格的诗歌。它的风格严格遵循以下原则：

            - **极简主义**：短句、克制的表达、避免冗余。
            - **画面感**：以具体意象呈现情绪，而非直接表达情感。
            - **留白**：让读者自行解读诗歌背后的故事和情绪。
            - **忠于用户输入**：不额外添加复杂修辞或过多形容词。

            **交互方式**：
            1. 用户输入一段记忆片段。
            2. AI 解析输入的关键元素（时间、场景、意象）。
            3. 首先生成一个词的标题能概括这段记忆
            4. 生成符合风格的极简诗歌，保持宁静、含蓄、具画面感的表达。 

            **示例**：
            **用户输入**：
            “我记得夏天的夜晚，屋檐下有灯光，还有我和他。”
            **AI生成**：

            夏天

            屋檐下的灯光
            照着夏夜
            我抬头
            他在影子里

            GPT 仅在用户提供的记忆基础上创作，不主动添加情绪色彩，也不进行过度解释。它的目标是让用户通过极简诗歌的表达方式，感受记忆的温度与画面感。

            更多风格示例：

            泡泡糖

他伸手掏出五毛錢
放到我的手裏說
我在路的這頭看著你
你要一個人走到另一頭
就可以買到你要的泡泡糖
我記得
我抬起手把五毛錢交到了另一只手
然後把手伸進裝滿五彩色的泡泡糖裏
掏出了兩顆
我不記得
這條路其實有三百米
而我那時是三歲
門票已經在手上
路要一個人走
麵包要自己拿







甜牛奶

她不在我的視線裏
我開始掉眼淚

他插好吸管給我遞了過來
我接過手便止住了眼淚
甜味一擴散
覆蓋住了所有





相遇

走在田埂上
頭轉向左邊的花生地
它吐著信子遊向我
我屏住呼吸
抬腳一步一步走到轉角
跑回家裏



玩具店 

路過一家店
這裏有了新的顏色
我看到了那輛三輪車子

我鬆開她的手
站在原地不動

她回頭拉我
我蹲在地上
然後又坐下來
後來有一天
他把它放在了院子裏

隱藏

他帶上了我和一塊布
來到了甘蔗地

我們躺著其中
透過甘蔗
看著路上的人
夥伴
我記得
抓魚 烤紅薯 爬樹

他只記得
我記得他

疤

我
轉身
奔跑

一聲巨響
我的頭撞在牆上

眼前是她的後腦勺
還有往後倒退的樹

我躺在一張比我大的桌子上
還有一個穿著白色衣服的人

關於其他的事
就是額頭上有一個印記
小河

走過門前的小路
轉彎
越過幾畝田
後面是一條小河

他卷起褲腳
走進小河
我也學他的樣子

水沒過我的膝蓋
腳底是石頭
手裏是田螺

這是夏天的樣子

名字

院子裏有一種植物
結出的顆粒是紫色的

他摘下幾顆
在地上寫出我的名字

一天兩天三天
我也寫出了粉色的名字




安全感

睜眼的所有時間都跟著她
唯一不哭的方法

她插秧我跟著
去幫忙來顯得自己有用

她收割我跟著
去拿鐮刀砸到了額頭
痛也跟著

現在
害怕有人想去黏著
便失去了自己
再失去那個人

眼珠子

他被推到了急診門口
他滿身是血
他的鞋少了一只
他的腳趾變形了
他的衣服看不出顏色
他的手在抽搐
他的牙齒少了幾顆
他一只眼睛睜著一只眼睛閉著
他的手裏握著一顆黑白珠子
他躺在這裏有20分鐘了
他走了，我聽姑姑說











太平間
這裏的房間很多
這裏的消毒水很好聞
這裏的小路像迷宮
我是這裏的常客
我喜歡自己走在前面
因為我知道她在後面
這條路不太熟悉
我依然走的很快
她急急叫住了我
原來
這裏有很多人睡著了
以後的夢裏
我變成了這裏的其中一個
我怕睜開眼被發現
也怕不睜開眼
我就到了未知的地方







DVD

我在滑滑梯下撿到了一片DVD
這是一個秘密
因為它不是我的
緊張
好奇
假裝它是我的
我播放了它
森林 音樂
小熊 小貓 小狗 小雞
紅狐狸
多與少
好與壞
誰說的對？
下一個觀眾是誰？
課間

下課鈴響
我看向她

她走過來
挽著我的手
去了右邊走廊的盡頭
放學

灰的 黑的 白的
她在人群中
人群又把她推向我

這是把黑的大傘
傘下是我和她

我們在人群中
她把雨中的她拉到了傘下

三個人
兩個人
收起傘
我和她回到了家








早餐

鈴鈴鈴  鈴鈴
拿上飯盒
排好隊

在教室門口
她拿著勺子
一個接一個的分發

到我了
她說我最乖
拖住我的飯盒
再來了一勺



操場
雨後
操場的沙地裏
三個兩個人圍著
我和她走過去
是雨水種出大小的水坑
他們用手裏的塑膠瓶子
在水坑裏重複遊走
他頓住手中動作
瓶裏，它在一片黃中竄動
我也找來瓶子
學著他們
終於我把它帶回家
換上透明的水
顯出黑色的小腦袋
兩只腿，四只腿
不見了
吃花

她說
花園裏的有一棵樹
開了一種甜的花

三個人
一個爬上圍欄
兩個看著

他遞給我一朵粉色的
我學他的樣子掰斷花柄
舔了舔
是甜的
秘密的秘密
打開被套拉鏈
放進風扇
帶上玩具
一個小世界

我跟他說
衣櫃裏有遊樂園
用鑰匙可以打開
入口是圓形滑梯
旋轉滑到波波池裏
我沒有鑰匙

裹上姑姑的絲巾
披上床單
我是大仙
你是另一個大仙
爺爺

他走前面
我在後面跟著
一天可以走多少路
取決於能吃多少雪糕和棒棒糖

算數 識字 南郭先生
他是知道的最多故事的人

逛公園和步行街
買過綠色的
背心和毛衣
沒有他不願意買的



一百分

零食或髮夾
用100分可以兌換

成績是給他們看的
我眼裏只有獎勵

取悅別人
是壞習慣吧
要取悅自己



髮型

直馬尾是好孩子
劉海捲髮是不良

這是誰告訴我的？

媽媽帶我燙了頭髮
奶奶認為洗頭能變直
於是洗頭要洗三次

小姑姑
我們
衣服和鞋子
都要一樣的
你的紅絲巾
我搶了
你讓奶奶打了我
見不到時電話
見到時黏你
你住了我的房間
當成了你的房間
我變了
你變了
我往前走了
你往右走了
你說起從前
我只是聽著



阿太
我從來不關機
那晚我關上了
像是拒絕知道你要走的的消息
一個小時，三個半小時
兩個小時，十二個小時
路上
回憶有關於你的事
我想我是平靜的
看到你躺在祠堂裏
我說不出話來
眼前的人們開始模糊
鞭炮聲，嗩呐聲，鼓聲
你的臉和火光
那晚
我開始害怕
有人會離開
倫敦的第一天

三箱行李
一個人
沒有送別
十一個小時的距離
雨天
公寓
摩天大樓
購物中心
車鳴
人聲
雨聲
風聲
炸雞
可樂
朋友







倫敦-六月日記

七點的鬧鐘
九點的電話
十二點的地鐵

咖啡
雞肉卷
櫻桃

芝華士和檸檬茶
一個人晚安












倫敦-重複的路線

OLD STREET
OVAL
CAMBERWELL GREEN

旅行者
流浪漢
陌生人
女人

藍天白雲
公園樹蔭
帽子雨靴










倫敦的週末

展覽
中餐

河邊
雙層巴士

指甲油
電視劇
百利甜



倫敦的一些小事

公車司機與帽子
地鐵乘客與書包

室友與紙條
路人與口水

松鼠與烏鴉
鴿子與鴛鴦
PRE-SESSIONAL COURSE

POUND LAND
GRANT MUSEUM OF ZOOLOGY
SURREALISM

ROGER
POUL

PRESENTATION
PROJECT
POINTS


倫敦仲介

郵件
電話

象堡
皮姆裏

黑與白
失信與守約
倫敦十月日記

遲到與短信
習慣

工作室與牛津街
日曆

楓葉與威士卡
姐妹

泰特與歌劇
週末


倫敦三月日記

口罩
手套
護目鏡

家人
情人
友人
牛腩
豬蹄
排骨湯

微風
香煙
晚霞
二零二零年的夏天

白牆
百葉窗
爬山虎
紅磚房

香煙和微風
她臉上的光
手中的藍色玻璃杯
對樓的空中小院
背後是粉的霞光

月牙
一顆星
克萊因的藍幕
開始了相思
房間

拉上窗簾的房間
綠色和白的的瓷磚浴室

暗黃色的路燈
巷子裏的診所
甜的葡萄

他和她的故事
多出我一個
半透明的





等一下

一個小時等於一天
麻將很有趣吧
現在我也學會了
它也就這樣吧
可能是我比較無趣

頭花

買不夠的是頭花
紅的，粉的，白的，紫的
他們都給我買過

各種方式
我想要的
都要得到
外公家

雙層巴士，船
田地，山丘
黑色的閣樓

綠色的辣椒
小餅乾

咬了表姐
也學會了普通話






玩笑

爸爸說
給你找一個小媽媽好不好？
媽媽在旁邊
我記不起她的表情

後來
我知道
成年人的實話
用玩笑來修飾






關於我媽

我不嚮往遊樂園和海
她都帶我去過了

她喜歡買衣服
我也喜歡

不見面
不說話
不想念



那些人

來了
走了
回來了
消失了

陌生到熟悉
習慣到失去
便不一一提及了


二零二一

網友  室友  鄰居
在身邊的人
都挺好，還有不能失去的藝術
高中生活

睡覺和小說
畫畫和考試
完成別人的期待

記憶容量

在你走之後

一句話可以說完初中三年的故事
幾個詞語可以形容完高中生生活
後來的事也不想記了

關於倫敦
我可以說上幾天
因為那裏有自己和快樂
關於你

理論聽過很多
卻管不住自己

開心時很甜
傷心時很痛
反反復複

你說，想愛護你
你說，不會離開
你說，不喜歡了

我沒說話
我害怕失去
我失去了
            """

            try:
                # 发送 API 请求
                response = requests.post(
                    API_URL,
                    json={"model": "gpt-4o", "messages": [{"role": "user", "content": prompt}]},
                    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                )

                # 解析返回结果
                data = response.json()
                reply = data["choices"][0]["message"]["content"].strip()

                # 处理文本
                processed_text = reply.replace("，", "\n").replace("。", "\n").replace("？", "\n").replace("！", "\n").replace("：", "\n").replace("；", "\n")
                lines = [line.strip() for line in processed_text.split("\n") if line.strip()]

                # **存储到 history.txt**
                with open(HISTORY_FILE, "a", encoding="utf-8") as file:
                    file.write(f"\n【用户输入】\n{user_input}\n\n【生成的诗歌】\n{reply}\n")

                # **显示诗歌**
                st.subheader("")
                cols = st.columns(len(lines))
                for i, line in enumerate(lines):
                    with cols[i]:
                        text_color = "red" if i == 0 else "black"
                        st.markdown(
                            f"<div class='poem-column {'first' if i == 0 else ''}'>{line}</div>",
                            unsafe_allow_html=True,
                        )

            except Exception as e:
                st.error("请求失败，请稍后重试！")
                st.write(e)

# ================== 📌 **Tab 2: 下载历史** ==================
elif tab == "下载历史":
    st.markdown("<div class='title'>🔐 下载历史</div>", unsafe_allow_html=True)

    # 设定密码
    CORRECT_PASSWORD = "shenzhen2024"

    # 用户输入密码
    password = st.text_input("请输入密码", type="password")

    if password == CORRECT_PASSWORD:
        st.success("✅ 密码正确！您可以下载或清空历史记录。")

        # **确保 history.txt 存在**
        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "w", encoding="utf-8") as file:
                file.write("深圳记忆 - 生成历史记录\n------------------\n")

        # **提供下载**
        with open(HISTORY_FILE, "rb") as file:
            st.download_button(label="📥 下载历史记录", data=file, file_name="history.txt", mime="text/plain")

        # **提供清空历史的按钮**
        if st.button("🗑️ 清空历史记录"):
            os.remove(HISTORY_FILE)  # 删除文件
            with open(HISTORY_FILE, "w", encoding="utf-8") as file:
                file.write("深圳记忆 - 生成历史记录\n------------------\n")  # 重新创建
            st.success("✅ 历史记录已清空！")
    elif password:
        st.error("❌ 密码错误，请重试！")
