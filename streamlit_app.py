import streamlit as st
import requests
import os
import json
import random
import time

# 设置页面布局，并默认折叠侧边栏
st.set_page_config(page_title="深圳记忆", layout="wide", initial_sidebar_state="collapsed")

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

# **创建左侧 Tab 选择**
tab = st.sidebar.radio("选择页面", ["深圳记忆", "下载历史", "诗歌弹幕"])

# ================== 📌 **Tab 1: 深圳记忆** ==================
if tab == "深圳记忆":
    st.markdown("<div class='title'>深圳记忆</div>", unsafe_allow_html=True)

    # 用户输入框
    user_input = st.text_area("", placeholder="请输入一段记忆...", key="memory_input")

    # 让提交按钮居中
    col1, col2, col3 = st.columns([3, 2, 3])  
    with col2:
        submit = st.button("提交", use_container_width=True)  

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

                # 存储到 JSON 格式的 history.txt
                with open(HISTORY_FILE, "a", encoding="utf-8") as file:
                    file.write(json.dumps({"user_input": user_input, "generated_poem": reply}, ensure_ascii=False) + "\n")

                st.success("✅ 诗歌已生成并保存！")

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
    st.markdown("""
    <style>
        .barrage-container { position: fixed; bottom: 0; left: 0; width: 100%; height: 100%; pointer-events: none; overflow: hidden; }
        .barrage-poem { position: absolute; font-size: 20px; font-weight: bold; color: #555; font-family: SimHei, sans-serif; animation: moveUp 24s linear infinite; }
        @keyframes moveUp { from { transform: translateY(100%); opacity: 1; } to { transform: translateY(-150%); opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

    if "last_poem_count" not in st.session_state:
        st.session_state.last_poem_count = 0  # 记录上次的诗歌数量

    placeholder = st.empty()  # 创建占位符

    # **自动更新弹幕**
    poems = load_poetry_history()
    if len(poems) > st.session_state.last_poem_count:
        selected_poems = random.sample(poems, min(len(poems), 5))  # 最多 5 首诗
        top_spacing = 20  # 每首诗间隔 20vh，防止重叠
        
        # **更新弹幕**
        barrage_html = "<div class='barrage-container'>"
        for i, poem in enumerate(selected_poems):
            x_pos = random.randint(10, 70)  # 随机水平位置
            speed = random.uniform(24, 40)  # 速度更慢
            top_position = i * top_spacing  # 计算初始位置，防止重叠
            align = "left" if x_pos < 30 else "right" if x_pos > 60 else "center"  # 对齐方式

            barrage_html += f"""
            <div class='barrage-poem' style='
                left:{x_pos}vw; 
                top:{top_position}vh; 
                animation-duration: {speed}s; 
                text-align: {align};'>
                {poem}
            </div>
            """
        barrage_html += "</div>"
        
        # **更新弹幕显示**
        placeholder.markdown(barrage_html, unsafe_allow_html=True)

        # **更新诗歌计数**
        st.session_state.last_poem_count = len(poems)

    # **自动刷新**
    time.sleep(5)  # 每 5 秒检查 `history.txt`
    st.rerun()
