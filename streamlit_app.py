import streamlit as st
import requests
import os
import json
import random

# 设置页面布局，并默认折叠侧边栏
st.set_page_config(page_title="深圳记忆", layout="wide", initial_sidebar_state="collapsed")

# **创建左侧 Tab 选择**
tab = st.sidebar.radio("选择页面", ["深圳记忆", "下载历史", "诗歌弹幕"])

# **历史记录文件路径**
HISTORY_FILE = "history.txt"
PROMPT_FILE = "prompt.txt"  # Prompt 文件路径

# **函数：读取 Prompt**
def read_prompt():
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    return "【错误】未找到 prompt.txt，请检查文件是否存在！"

# ================== 📌 **Tab 1: 深圳记忆** ==================
if tab == "深圳记忆":
    # 读取状态，决定是否进入简约模式
    if "show_poem" not in st.session_state:
        st.session_state.show_poem = False
    if "memory_input" not in st.session_state:
        st.session_state.memory_input = ""

    # **如果未提交，显示输入框**
    if not st.session_state.show_poem:
        st.markdown(
            """
            <style>
            .title {
                font-family: SimHei, sans-serif;
                font-size: 20px;
                color: #666;
                text-align: center;
                font-weight: normal;
            }
            div[data-testid="stTextArea"] {
                display: flex;
                justify-content: center;
            }
            div[data-testid="stTextArea"] > div {
                width: 250px !important;
                margin: auto !important;
            }
            div[data-testid="stTextArea"] textarea {
                width: 100%;
                min-height: 30px;
                text-align: center;
                border: 2px dashed #bbb;
                border-radius: 5px;
                font-family: SimHei, sans-serif;
                font-size: 16px;
                padding: 5px;
            }
            .button-container {
                display: flex;
                justify-content: center;
                margin-top: 10px;
            }
            div[data-testid="stButton"] button {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                background-color: #bbb;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border: none;
            }
            .home-text {
                text-align: center;
                font-family: SimHei, sans-serif;
                font-size: 16px;
                color: #666;
                margin-top: 10px;
            }
            </style>
            <div class='title'>关于你的深圳记忆<br>About Your Shenzhen Memory</div>
            """,
            unsafe_allow_html=True
        )

        user_input = st.text_area("", placeholder="输入 Type", key="memory_input")

        submit = st.button("OK")

        if submit:
            if not user_input.strip():
                st.warning("请输入内容后再提交！")
            else:
                st.session_state.memory_input = user_input
                st.session_state.show_poem = True
                st.rerun()

        # 显示 Home 和 家
        st.markdown("<div class='home-text'>Home</div><div class='home-text'>家</div>", unsafe_allow_html=True)

    # **如果 OK 被按下，显示简约模式**
    else:
        st.markdown(f"<div class='title'>{st.session_state.memory_input}</div>", unsafe_allow_html=True)

        API_KEY = st.secrets["api"]["key"]
        API_URL = "https://api2.aigcbest.top/v1/chat/completions"

        base_prompt = read_prompt()
        full_prompt = f"**用户输入**：\n{st.session_state.memory_input}\n\n{base_prompt}"

        try:
            response = requests.post(
                API_URL,
                json={"model": "gpt-4o", "messages": [{"role": "user", "content": full_prompt}]},
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            )
            data = response.json()
            reply = data["choices"][0]["message"]["content"].strip()

            # **处理诗歌格式**
            processed_text = reply.replace("，", "\n").replace("。", "\n").replace("？", "\n").replace("！", "\n").replace("：", "\n").replace("；", "\n")
            lines = [line.strip() for line in processed_text.splitlines() if line.strip()]

            # **存储历史记录**
            with open(HISTORY_FILE, "a", encoding="utf-8") as file:
                file.write(json.dumps({"user_input": st.session_state.memory_input, "generated_poem": reply}, ensure_ascii=False) + "\n")

            # **显示诗歌**
            st.markdown("<div class='poem-container'>", unsafe_allow_html=True)
            for line in lines:
                st.markdown(f"<p>{line}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error("请求失败，请稍后重试！")
            st.write(e)

# ================== 📌 **Tab 2: 下载历史**（不变）
elif tab == "下载历史":
    st.markdown("<div class='title'>🔐 下载历史</div>", unsafe_allow_html=True)

    CORRECT_PASSWORD = "shenzhen2024"
    password = st.text_input("请输入密码", type="password")

    if password == CORRECT_PASSWORD:
        st.success("✅ 密码正确！您可以下载或清空历史记录。")

        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "w", encoding="utf-8") as file:
                file.write("")

        with open(HISTORY_FILE, "rb") as file:
            st.download_button(label="📥 下载历史记录 (JSON)", data=file, file_name="history.json", mime="application/json")

        if st.button("🗑️ 清空历史记录"):
            os.remove(HISTORY_FILE)
            with open(HISTORY_FILE, "w", encoding="utf-8") as file:
                file.write("")
            st.success("✅ 历史记录已清空！")
    elif password:
        st.error("❌ 密码错误，请重试！")

# ================== 📌 **Tab 3: 诗歌弹幕**（不变）
elif tab == "诗歌弹幕":
    poems = load_poetry_history()
    if not poems:
        st.warning("📌 目前没有历史记录，请先在'深圳记忆'中提交诗歌！")
    else:
        num_poems = min(len(poems), 10)
        st.markdown("<div class='barrage-container'>", unsafe_allow_html=True)
    
        for poem in random.sample(poems, num_poems):
            st.markdown(f"<div class='barrage-poem'>{poem}</div>", unsafe_allow_html=True)
    
        st.markdown("</div>", unsafe_allow_html=True)
