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
            pointer-events: none;
            overflow: hidden;
        }

        /* 每个完整的诗歌块 */
        .barrage-poem {
            position: absolute;
            font-size: 20px;
            font-family: SimHei, sans-serif;
            color: #555;
            animation: moveUp 20s linear infinite; /* 统一向上移动 */
            white-space: pre-line;
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

# **初始化 session_state**
if "poetry_history" not in st.session_state:
    st.session_state["poetry_history"] = []  # 诗歌列表
    st.session_state["last_loaded"] = 0  # 记录最后读取的行数

# **函数：读取 Prompt**
def read_prompt():
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    return "【错误】未找到 prompt.txt，请检查文件是否存在！"

# **函数：读取历史诗歌**
def load_new_poetry():
    if not os.path.exists(HISTORY_FILE):
        return []
    
    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()
        new_poems = [json.loads(line)["generated_poem"] for line in lines[st.session_state["last_loaded"]:] if line.strip()]
        st.session_state["last_loaded"] = len(lines)  # 记录已读取的行数
        return new_poems

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

                # 存储
                with open(HISTORY_FILE, "a", encoding="utf-8") as file:
                    file.write(json.dumps({"user_input": user_input, "generated_poem": reply}, ensure_ascii=False) + "\n")

                # 立即更新 `session_state`，让弹幕能立刻加载新诗歌
                st.session_state["poetry_history"].append(reply)

                st.success("✅ 诗歌已保存！")

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
    # 加载新诗歌
    new_poems = load_new_poetry()
    st.session_state["poetry_history"].extend(new_poems)  # 追加新诗歌

    if not st.session_state["poetry_history"]:
        st.warning("📌 目前没有历史记录，请先在'深圳记忆'中提交诗歌！")
    else:
        # 只显示最近 5 首
        selected_poems = st.session_state["poetry_history"][-5:]
        top_spacing = 20  # 控制每首诗的间隔

        # 显示弹幕效果
        st.markdown("<div class='barrage-container'>", unsafe_allow_html=True)
        for i, poem in enumerate(selected_poems):
            x_pos = random.randint(10, 70)  # 随机水平位置
            speed = random.uniform(25, 40)  # 速度
            top_position = i * top_spacing  # 计算初始位置，防止重叠
            align = "left" if x_pos < 30 else "right" if x_pos > 60 else "center"  # 对齐方式

            st.markdown(
                f"""
                <div class='barrage-poem' style='
                    left:{x_pos}vw; 
                    top:{top_position}vh; 
                    animation-duration: {speed}s; 
                    text-align: {align};'>
                    {poem}
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # **自动刷新（5 秒轮询一次）**
    st.experimental_rerun() if "st_autorefresh" not in globals() else st_autorefresh(interval=5000)
