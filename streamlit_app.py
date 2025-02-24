import streamlit as st
import requests
import os

# 设置页面布局，并隐藏 Streamlit 默认 UI
st.set_page_config(page_title="深圳记忆", layout="wide")

# **历史记录文件路径**
HISTORY_FILE = "history.txt"

# **创建隐藏侧边栏的控制变量**
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False

# **菜单按钮（点击后切换菜单显示状态）**
col1, col2, col3 = st.columns([1, 2, 1])  # 让按钮居中
with col2:
    if st.button("📂 显示菜单" if not st.session_state.show_sidebar else "❌ 隐藏菜单"):
        st.session_state.show_sidebar = not st.session_state.show_sidebar

# **动态创建侧边栏（仅在状态为 True 时显示）**
if st.session_state.show_sidebar:
    tab = st.sidebar.radio("选择页面", ["深圳记忆", "下载历史"])
else:
    tab = "深圳记忆"  # 默认进入「深圳记忆」页面

# ================== 📌 **Tab 1: 深圳记忆** ==================
if tab == "深圳记忆":
    st.markdown("<h1 style='text-align: center;'>深圳记忆</h1>", unsafe_allow_html=True)

    # 用户输入框
    user_input = st.text_area("", placeholder="请输入一段记忆...", key="memory_input")

    # **让提交按钮居中**
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit = st.button("📩 提交记忆")

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
                        f"<div style='writing-mode: vertical-rl; text-align: center; font-size: 24px; font-weight: bold; color: {text_color}; background-color: white;'>{line}</div>",
                        unsafe_allow_html=True,
                    )

        except Exception as e:
            st.error("请求失败，请稍后重试！")
            st.write(e)

# ================== 📌 **Tab 2: 下载历史** ==================
elif tab == "下载历史":
    st.markdown("<h1 style='text-align: center;'>🔐 下载历史</h1>", unsafe_allow_html=True)

    # 设定密码
    CORRECT_PASSWORD = "shenzhen2024"

    # 用户输入密码
    password = st.text_input("请输入密码", type="password")

    if password == CORRECT_PASSWORD:
        st.success("✅ 密码正确！您可以下载或清空历史记录。")

        # **使用 `st.expander()` 折叠历史管理**
        with st.expander("📂 管理历史记录", expanded=True):

            # **确保 history.txt 存在**
            if not os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, "w", encoding="utf-8") as file:
                    file.write("深圳记忆 - 生成历史记录\n------------------\n")

            # **提供下载**
            with open(HISTORY_FILE, "rb") as file:
                st.download_button("📥 下载历史记录", file, file_name="history.txt")

            # **提供清空历史的按钮**
            colA, colB, colC = st.columns([1, 2, 1])  # 让按钮居中
            with colB:
                if st.button("🗑️ 清空历史记录"):
                    os.remove(HISTORY_FILE)
                    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
                        file.write("深圳记忆 - 生成历史记录\n------------------\n")
                    st.success("✅ 历史记录已清空！")

    elif password:
        st.error("❌ 密码错误，请重试！")
