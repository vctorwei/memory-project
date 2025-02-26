import streamlit as st
import requests
import os
import json
import random

# 设置页面布局，并默认折叠侧边栏
st.set_page_config(page_title="深圳记忆", layout="wide", initial_sidebar_state="collapsed")

# CSS 样式 - 弹幕
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;} /* 隐藏 Streamlit 右上角菜单 */
        header {visibility: hidden;} /* 隐藏 Streamlit 默认标题栏 */

        /* 弹幕容器 */
        .barrage-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none; /* 让弹幕不会影响点击操作 */
            overflow: hidden;
        }

        /* 每个完整的诗歌块 */
        .barrage-poem {
            position: absolute;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 8px;
            padding: 10px;
            white-space: pre-line;
            opacity: 1;
            animation: moveUp 12s linear infinite; /* 统一向上移动 */
        }

        /* 动画：诗歌整体向上移动 */
        @keyframes moveUp {
            from {
                transform: translateY(100%);
                opacity: 1;
            }
            to {
                transform: translateY(-150%);
                opacity: 0;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

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

# **函数：读取历史诗歌**
def load_poetry_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
            poems = [json.loads(line)["generated_poem"] for line in lines if line.strip()]
            return poems
    return []

# ================== 📌 **Tab 1: 深圳记忆** ==================
if tab == "深圳记忆":
if tab == "深圳记忆":
    st.markdown(
        """
        <style>
        .title {
            font-family: SimHei, sans-serif;
            font-size: 20px; /* 调小字号 */
            font-weight: bold;
            color: #666; /* 灰色字体 */
            text-align: center;
        }
        .custom-input textarea {
            text-align: center; /* 输入框文字居中 */
            font-family: SimHei, sans-serif;
        }
        .custom-button {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 60px; /* 按钮大小 */
            height: 60px;
            border-radius: 50%; /* 圆形按钮 */
            background-color: #bbb; /* 灰色 */
            color: white;
            font-weight: bold;
            font-size: 16px;
            border: none;
            cursor: pointer;
        }
        </style>
        <div class='title'>关于你的深圳记忆<br>About Your Shenzhen Memory</div>
        """,
        unsafe_allow_html=True
    )

    # 用户输入框（带居中 CSS）
    user_input = st.text_area("", placeholder="输入 Type", key="memory_input", help="请输入一段记忆...")

    # 让提交按钮居中
    col1, col2, col3 = st.columns([3, 2, 3])  
    with col2:
        submit = st.markdown('<button class="custom-button">OK</button>', unsafe_allow_html=True)

    API_KEY = st.secrets["api"]["key"]
    API_URL = "https://api2.aigcbest.top/v1/chat/completions"


    if submit:
        if not user_input.strip():
            st.warning("请输入内容后再提交！")
        else:
            base_prompt = read_prompt()
            full_prompt = f"**用户输入**：\n{user_input}\n\n{base_prompt}"

            try:
                response = requests.post(
                    API_URL,
                    json={"model": "gpt-4o", "messages": [{"role": "user", "content": full_prompt}]},
                    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                )
                data = response.json()
                reply = data["choices"][0]["message"]["content"].strip()

                # 处理文本
                processed_text = reply.replace("，", "\n").replace("。", "\n").replace("？", "\n").replace("！", "\n").replace("：", "\n").replace("；", "\n")
                lines = [line.strip() for line in processed_text.splitlines() if line.strip()] 

                # 存储
                with open(HISTORY_FILE, "a", encoding="utf-8") as file:
                    file.write(json.dumps({"user_input": user_input, "generated_poem": reply}, ensure_ascii=False) + "\n")

                # **显示诗歌**
                st.subheader("")
                st.markdown("<div class='poem-container'>", unsafe_allow_html=True)  
                cols = st.columns(len(lines))  
                for i, line in enumerate(reversed(lines)):  
                    with cols[i]:
                        st.markdown(
                            f"<div class='poem-column {'first' if i == len(lines) - 1 else ''}'>{line}</div>",
                            unsafe_allow_html=True,
                        )
                st.markdown("</div>", unsafe_allow_html=True)  

            except Exception as e:
                st.error("请求失败，请稍后重试！")
                st.write(e)

# ================== 📌 **Tab 2: 下载历史** ==================
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

# ================== 📌 **Tab 3: 诗歌弹幕** ==================
elif tab == "诗歌弹幕":
    poems = load_poetry_history()
    if not poems:
        st.warning("📌 目前没有历史记录，请先在'深圳记忆'中提交诗歌！")
    else:
        selected_poems = random.sample(poems, min(len(poems), 5))  # 最多 5 首诗
        top_spacing = 20  # 每首诗间隔 20vh，防止重叠

        # 显示弹幕效果
        st.markdown("<div class='barrage-container'>", unsafe_allow_html=True)
        for i, poem in enumerate(selected_poems):
            x_pos = random.randint(10, 70)  # 随机水平位置
            speed = random.uniform(16, 28)  # 速度
            top_position = i * top_spacing  # 计算初始位置，防止重叠
            align = "left" if x_pos < 30 else "right" if x_pos > 60 else "center"  # 对齐方式

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
