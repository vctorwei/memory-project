import streamlit as st
import requests
import os

# 设置页面布局，并默认折叠侧边栏
st.set_page_config(page_title="深圳记忆", layout="wide", initial_sidebar_state="collapsed")

# 使用 CSS 隐藏 Streamlit 菜单、页脚和标题栏
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .title {
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
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
PROMPT_FILE = "prompt.txt"  # Prompt 文件路径

# **函数：读取 Prompt**
def read_prompt():
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    return "【错误】未找到 prompt.txt，请检查文件是否存在！"

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
            # 读取 Prompt 并替换用户输入
            base_prompt = read_prompt()
            prompt = base_prompt.replace("{USER_INPUT}", user_input)

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
