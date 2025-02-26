import streamlit as st
import requests
import os
import json
import random

# 设置页面布局
st.set_page_config(page_title="深圳记忆", layout="wide", initial_sidebar_state="collapsed")

# 自定义 CSS 样式
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;} /* 隐藏 Streamlit 右上角菜单 */
        header {visibility: hidden;} /* 隐藏 Streamlit 默认标题栏 */

        /* 标题样式 */
        .title {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
        }

        .subtitle {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 40px;
        }

        /* 输入框样式 */
        .custom-input-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }

        .custom-input {
            width: 50%;
            padding: 10px;
            font-size: 18px;
            border: 2px dashed #ccc;
            border-radius: 8px;
            text-align: center;
        }

        /* 按钮样式 */
        .ok-button-container {
            display: flex;
            justify-content: center;
            margin-bottom: 40px;
        }

        .ok-button {
            width: 60px;
            height: 60px;
            line-height: 60px;
            border-radius: 50%;
            text-align: center;
            font-size: 18px;
            background-color: #e0e0e0;
            color: black;
            border: none;
            cursor: pointer;
        }

        /* Home 样式 */
        .home-text {
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .home-text-chinese {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# **Tab 选择**
tab = st.sidebar.radio("选择页面", ["深圳记忆", "下载历史", "诗歌弹幕"])

# ================== 📌 **Tab 1: 深圳记忆（UI 调整）** ==================
if tab == "深圳记忆":
    st.markdown("<div class='title'>关于你的深圳记忆</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>About Your Shenzhen Memory</div>", unsafe_allow_html=True)

    # 空两行
    st.write("")
    st.write("")

    # **输入框**
    st.markdown("<div class='custom-input-container'>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="输入 Type", key="memory_input")
    st.markdown("</div>", unsafe_allow_html=True)

    # **OK 按钮**
    st.markdown("<div class='ok-button-container'>", unsafe_allow_html=True)
    submit = st.button("OK", key="ok_button")
    st.markdown("</div>", unsafe_allow_html=True)

    # 空两行
    st.write("")
    st.write("")

    # **Home / 家**
    st.markdown("<div class='home-text'>Home</div>", unsafe_allow_html=True)
    st.markdown("<div class='home-text-chinese'>家</div>", unsafe_allow_html=True)

# ================== 📌 **Tab 2: 下载历史（保持原功能不变）** ==================
elif tab == "下载历史":
    st.markdown("<div class='title'>🔐 下载历史</div>", unsafe_allow_html=True)

    CORRECT_PASSWORD = "shenzhen2024"
    password = st.text_input("请输入密码", type="password")

    if password == CORRECT_PASSWORD:
        st.success("✅ 密码正确！您可以下载或清空历史记录。")

        HISTORY_FILE = "history.txt"
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

# ================== 📌 **Tab 3: 诗歌弹幕（保持原功能不变）** ==================
elif tab == "诗歌弹幕":
    HISTORY_FILE = "history.txt"

    def load_poetry_history():
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                lines = file.readlines()
                poems = [json.loads(line)["generated_poem"] for line in lines if line.strip()]
                return poems
        return []

    poems = load_poetry_history()
    if not poems:
        st.warning("📌 目前没有历史记录，请先在'深圳记忆'中提交诗歌！")
    else:
        selected_poems = random.sample(poems, min(len(poems), 5))
        top_spacing = 20

        st.markdown("<div class='barrage-container'>", unsafe_allow_html=True)
        for i, poem in enumerate(selected_poems):
            x_pos = random.randint(10, 70)
            speed = random.uniform(16, 28)
            top_position = i * top_spacing
            align = "left" if x_pos < 30 else "right" if x_pos > 60 else "center"

            st.markdown(
                f"""
                <div class='barrage-poem' style='
                    left:{x_pos}vw; 
                    top:{top_position}vh; 
                    animation-duration: {speed}s; 
                    text-align: {align}; 
                    font-family: SimHei, sans-serif; 
                    font-size: 20px; 
                    color: #555;'>
                    {poem}
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
