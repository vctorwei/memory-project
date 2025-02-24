import streamlit as st
import requests
import os

# 设置页面布局，并隐藏 Streamlit 默认 UI
st.set_page_config(page_title="深圳记忆", layout="wide")

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

        /* 提交按钮居中 */
        .stButton {
            display: flex;
            justify-content: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# **历史记录文件路径**
HISTORY_FILE = "history.txt"

# **侧边栏开关**
toggle_sidebar = st.toggle("📂", value=False)

# **如果用户点击，显示侧边栏，否则隐藏**
if toggle_sidebar:
    tab = st.sidebar.radio("选择页面", ["深圳记忆", "下载历史"])
else:
    tab = "深圳记忆"  # 默认进入「深圳记忆」页面

# ================== 📌 **Tab 1: 深圳记忆** ==================
if tab == "深圳记忆":
    st.markdown("<div class='title'>深圳记忆</div>", unsafe_allow_html=True)

    # 用户输入框
    user_input = st.text_area("", placeholder="请输入一段记忆...", key="memory_input")

    # 让提交按钮居中
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit = st.button("提交")

    # **如果用户提交，存入历史**
    if submit and user_input.strip():
        # 生成 Prompt
        prompt = f"""
        **用户输入**：{user_input}

        解析用户输入的记忆片段，并生成极简风格的诗歌。风格要求：
        - **极简主义**：短句、克制的表达、避免冗余。
        - **画面感**：以具体意象呈现情绪，而非直接表达情感。
        - **留白**：让读者自行解读诗歌背后的故事和情绪。
        - **忠于用户输入**：不额外添加复杂修辞或过多形容词。
        """

        try:
            # 读取 API Key（从 Streamlit secrets 读取）
            API_KEY = st.secrets["api"]["key"]
            API_URL = "https://api2.aigcbest.top/v1/chat/completions"

            # 发送 API 请求
            response = requests.post(
                API_URL,
                json={"model": "gpt-4o", "messages": [{"role": "user", "content": prompt}]},
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            )

            # 解析返回结果
            data = response.json()
            reply = data["choices"][0]["message"]["content"].strip()

            # 处理文本：按标点分割，并去除标点
            processed_text = reply.replace("，", "\n").replace("。", "\n").replace("？", "\n").replace("！", "\n").replace("：", "\n").replace("；", "\n")
            lines = [line.strip() for line in processed_text.split("\n") if line.strip()]

            # **存入历史**
            with open(HISTORY_FILE, "a", encoding="utf-8") as file:
                file.write(f"\n【用户输入】\n{user_input}\n\n【生成的诗歌】\n{reply}\n")

            # **显示生成的诗歌**
            st.success("✅ 记忆已提交！")
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
            st.download_button("📥 下载历史记录", file, file_name="history.txt")

        # **提供清空历史的按钮**
        if st.button("🗑️ 清空历史记录"):
            os.remove(HISTORY_FILE)
            with open(HISTORY_FILE, "w", encoding="utf-8") as file:
                file.write("深圳记忆 - 生成历史记录\n------------------\n")
            st.success("✅ 历史记录已清空！")

    elif password:
        st.error("❌ 密码错误，请重试！")
