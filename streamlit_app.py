import streamlit as st
import requests
import os
import json
import random

# 设置页面布局
st.set_page_config(page_title="关于你的深圳记忆", layout="wide", initial_sidebar_state="collapsed")

# CSS 样式
st.markdown(
    """
    <style>
        #MainMenu, header, footer {visibility: hidden;} /* 隐藏 Streamlit 默认菜单 */

        /* 标题样式 */
        .title {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: gray;
            font-family: "SimHei", sans-serif;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: gray;
            font-family: "SimHei", sans-serif;
            margin-bottom: 40px;
        }

        /* 输入框样式 */
        .dashed-input input {
            border: 2px dashed gray !important;
            padding: 12px;
            text-align: center;
            font-size: 16px;
            width: 100%;
            border-radius: 5px;
            font-family: "SimHei", sans-serif;
        }

        /* 居中输入框 */
        .input-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }

        /* 圆形按钮 */
        .circle-button {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 10px;
        }
        
        .circle-button button {
            border-radius: 50%; /* 让按钮成为圆形 */
            width: 60px; /* 设定固定宽高 */
            height: 60px;
            background-color: gray;
            border: none;
            font-size: 18px;
            font-weight: bold;
            color: white;
            font-family: "SimHei", sans-serif;
            cursor: pointer;
            display: flex; 
            justify-content: center; 
            align-items: center;
        }


        /* 居中文本 */
        .center-text {
            text-align: center;
            font-size: 24px;
            margin-top: 30px;
            font-weight: bold;
            color: gray;
            font-family: "SimHei", sans-serif;
        }

        /* 弹幕容器 */
        .barrage-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
        }

        /* 弹幕动画 */
        .barrage-poem {
            position: absolute;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: black;
            font-family: "SimHei", sans-serif;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 8px;
            padding: 10px;
            white-space: pre-line;
            opacity: 1;
            animation: moveUp 12s linear infinite;
        }

        @keyframes moveUp {
            from { transform: translateY(100%); opacity: 1; }
            to { transform: translateY(-150%); opacity: 0; }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# **创建左侧 Tab 选择**
tab = st.sidebar.radio("选择页面", ["深圳记忆", "下载历史", "诗歌弹幕"])

# **历史记录文件路径**
HISTORY_FILE = "history.txt"
PROMPT_FILE = "prompt.txt"

# **读取 Prompt**
def read_prompt():
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    return "【错误】未找到 prompt.txt，请检查文件是否存在！"

# **读取历史诗歌**
def load_poetry_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
            poems = [json.loads(line)["generated_poem"] for line in lines if line.strip()]
            return poems
    return []

# ================== 📌 **Tab 1: 深圳记忆** ==================
if tab == "深圳记忆":
    st.markdown("<div class='title'>关于你的深圳记忆</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>About Your Shenzhen Memory</div>", unsafe_allow_html=True)

    # 空两行
    st.write("\n\n")

    # 用户输入框
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="输入 Type", key="memory_input")
    st.markdown("</div>", unsafe_allow_html=True)

    # 圆形按钮
    st.markdown('<div class="circle-button">', unsafe_allow_html=True)
    if st.button("OK"):
        st.success("提交成功！")
    st.markdown("</div>", unsafe_allow_html=True)

    # 空两行
    st.write("\n\n")

    # Home & 家
    st.markdown("<div class='center-text'>Home</div>", unsafe_allow_html=True)
    st.markdown("<div class='center-text'>家</div>", unsafe_allow_html=True)

# ================== 📌 **Tab 2: 下载历史** ==================
elif tab == "下载历史":
    st.markdown("<div class='title'>🔐 下载历史</div>", unsafe_allow_html=True)

    CORRECT_PASSWORD = "shenzhen2024"
    password = st.text_input("请输入密码", type="password")

    if password == CORRECT_PASSWORD:
        st.success("✅ 密码正确！")

        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "rb") as file:
                st.download_button(label="📥 下载历史记录 (JSON)", data=file, file_name="history.json", mime="application/json")

        if st.button("🗑️ 清空历史记录"):
            os.remove(HISTORY_FILE)
            with open(HISTORY_FILE, "w", encoding="utf-8") as file:
                file.write("")
            st.success("✅ 历史记录已清空！")
    elif password:
        st.error("❌ 密码错误，请重试！")

# ================== 📌 **Tab 3: 诗歌弹幕** ==================
elif tab == "诗歌弹幕":
    poems = load_poetry_history()
    if poems:
        st.markdown("<div class='barrage-container'>", unsafe_allow_html=True)
        for poem in poems:
            st.markdown(f"<div class='barrage-poem'>{poem}</div>", unsafe_allow_html=True)
    else:
        st.warning("暂无诗歌记录。")
