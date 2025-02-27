import streamlit as st
import requests
import os
import json
import random

# 设置页面布局，并默认折叠侧边栏
st.set_page_config(page_title="深圳记忆", layout="wide", initial_sidebar_state="collapsed")

# 全局隐藏 header 和 footer
st.markdown("""
    <style>
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    </style>
""", unsafe_allow_html=True)

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
    st.markdown(
        """
        <style>
        /* 隐藏 Streamlit 默认 UI */
        header, footer {visibility: hidden !important;}
        div[data-testid="stToolbar"] { display: none !important; }
        div[data-testid="stStatusWidget"] { display: none !important; }

        /* 标题样式 */
        .title {
            font-family: SimHei, sans-serif;
            font-size: 20px;
            color: #666;
            text-align: center;
            font-weight: normal;
        }
        /* 让输入框整体居中 */
        div[data-testid="stTextArea"] {
            display: flex;
            justify-content: center;
        }
        /* 让输入框本身变窄 + 居中 */
        div[data-testid="stTextArea"] > div {
            width: 250px !important;
            margin: auto !important;
        }
        /* 输入框内部样式 */
        div[data-testid="stTextArea"] textarea {
            width: 100% !important;
            min-height: 30px !important;
            height: 30px !important;
            max-height: 100px !important;
            overflow-y: hidden !important;
            resize: none !important;
            text-align: center !important;
            font-family: SimHei, sans-serif;
            font-size: 16px;
            border: 2px dashed #bbb !important;
            border-radius: 5px;
            padding: 5px;
            line-height: 20px !important;
            background-color: transparent !important;
        }
        /* 让 OK 按钮居中 */
        div[data-testid="stButton"] {
            display: flex;
            justify-content: center;
        }
        div[data-testid="stButton"] button {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background-color: #bbb !important;
            color: white !important;
            font-weight: bold;
            font-size: 16px;
            border: none;
            cursor: pointer;
            text-align: center;
            line-height: 16px;
        }
        /* Home 和 家 居中 */
        .home-text {
            text-align: center;
            font-family: SimHei, sans-serif;
            font-size: 16px;
            color: #666;
            margin-top: 10px;
        }
        /* 记忆文本样式 */
        .memory-text {
            text-align: center;
            font-family: SimHei, sans-serif;
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-top: 30px;
        }
        /* 诗歌容器 */
        .poem-container {
            text-align: center;
            font-family: SimHei, sans-serif;
            font-size: 16px;
            color: #444;
            margin-top: 20px;
            white-space: pre-line;
        }
        </style>
        <div class='title'>关于你的深圳记忆<br>About Your Shenzhen Memory</div>
        """,
        unsafe_allow_html=True
    )

    # 记录页面状态
    if "submitted" not in st.session_state:
        st.session_state["submitted"] = False

    if not st.session_state["submitted"]:
        # **按下 OK 之前，页面保持原样**
        user_input = st.text_area("", placeholder="输入 Type", key="memory_input")

        submit = st.button("OK")

        # Home/家 显示
        st.markdown(
            """
            <div class='home-text'>Home</div>
            <div class='home-text'>家</div>
            """,
            unsafe_allow_html=True
        )

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

                    # 格式化诗歌
                    processed_text = reply.replace("，", "\n").replace("。", "\n").replace("？", "\n").replace("！", "\n").replace("：", "\n").replace("；", "\n")
                    lines = [line.strip() for line in processed_text.splitlines() if line.strip()]

                    # 存储
                    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
                        file.write(json.dumps({"user_input": user_input, "generated_poem": reply}, ensure_ascii=False) + "\n")

                    # 保存状态
                    st.session_state["submitted"] = True
                    st.session_state["memory"] = user_input
                    st.session_state["poem"] = "\n".join(lines)

                    st.rerun()

                except Exception as e:
                    st.error("请求失败，请稍后重试！")
                    st.write(e)

    else:
        # **按下 OK 之后，页面变简约**
        st.markdown(f"<div class='memory-text'>{st.session_state['memory']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='poem-container'>{st.session_state['poem']}</div>", unsafe_allow_html=True)


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
    poems = load_poetry_history()
    if not poems:
        st.warning("📌 目前没有历史记录，请先在'深圳记忆'中提交诗歌！")
    else:
        num_poems = min(len(poems), 5)  # 最多 10 条弹幕
        screen_width = 95  # 屏幕宽度范围（vw）
        screen_height = 90  # 屏幕高度范围（vh）
    
        # 计算均匀分布的起始点
        spacing_x = screen_width // num_poems  # 计算横向间距
        spacing_y = screen_height // num_poems  # 计算纵向间距
    
        used_positions = set()  # 存储已经使用的坐标
    
        st.markdown("<div class='barrage-container'>", unsafe_allow_html=True)
    
        for i, poem in enumerate(random.sample(poems, num_poems)):
            # 计算大致均匀的位置
            base_x = i * spacing_x + random.randint(-10, 10)  # 允许小范围偏移
            base_y = i * spacing_y + random.randint(-10, 10)
    
            # 确保不会超出屏幕边界
            x_pos = max(5, min(base_x, screen_width - 5))
            y_pos = max(5, min(base_y, screen_height - 5))
    
            # 防止过度重叠（若位置太接近，则重新计算）
            while (x_pos, y_pos) in used_positions:
                x_pos += random.randint(-5, 5)
                y_pos += random.randint(-5, 5)
            used_positions.add((x_pos, y_pos))  # 记录已使用的位置
    
            speed = random.uniform(25, 45)  # 弹幕速度
            opacity = random.uniform(0.6, 1)  # 透明度
            font_size = random.randint(18, 26)  # 文字大小
    
            st.markdown(
                f"""
                <div class='barrage-poem' style='
                    left:{x_pos}vw; 
                    top:{y_pos}vh; 
                    animation-duration: {speed}s; 
                    opacity: {opacity}; 
                    font-size: {font_size}px;
                    font-family: SimHei, sans-serif;
                    color: #333;'>
                    {poem}
                </div>
                """,
                unsafe_allow_html=True,
            )
    
        st.markdown("</div>", unsafe_allow_html=True)
