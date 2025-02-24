import streamlit as st
import requests
import os
import json

# 设置页面布局，并默认折叠侧边栏
st.set_page_config(page_title="深圳记忆", layout="wide", initial_sidebar_state="collapsed")

# 使用 CSS 进行优化
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;} /* 隐藏 Streamlit 右上角菜单 */
        header {visibility: hidden;} /* 隐藏 Streamlit 默认标题栏 */

        /* 页面整体居中 */
        .block-container {
            padding-top: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* 标题居中 */
        .title {
            font-size: 40px;
            font-weight: normal;
            font-family: SimSun, serif; /* 设为宋体 */
            text-align: center;
            margin-bottom: 20px;
        }

        /* 诗歌部分靠右 */
        .poem-container {
            width: 100%;
            display: flex;
            justify-content: flex-end; /* 诗歌靠右对齐 */
        }

        /* 诗歌内容竖排 */
        .poem-column {
            writing-mode: vertical-rl;
            text-align: right;
            font-size: 24px;
            font-weight: normal; /* 取消加粗 */
            font-family: SimSun, serif; /* 设为宋体 */
            color: black;
            background-color: white;
            padding: 2px; /* 减少上下内边距，使行距更紧凑 */
            margin: 1px; /* 适当减少行间距 */
            display: inline-block;
            line-height: 1; /* 控制行高，使诗歌更紧凑 */
        }

        /* 最右侧的第一列变红 */
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

# **函数：保存 JSON 记录**
def save_to_history(user_input, generated_poem):
    history_entry = {
        "user_input": user_input,
        "generated_poem": generated_poem
    }
    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(history_entry, ensure_ascii=False) + "\n")

# ================== 📌 **Tab 1: 深圳记忆** ==================
if tab == "深圳记忆":
    st.markdown("<div class='title'>深圳记忆</div>", unsafe_allow_html=True)

    # 用户输入框
    user_input = st.text_area("", placeholder="请输入一段记忆...", key="memory_input")

    # 让提交按钮居中
    col1, col2, col3 = st.columns([3, 2, 3])  # 左右两侧列宽大一点，中间列小一点
    with col2:
        submit = st.button("提交", use_container_width=True)  # 让按钮宽度填充列

    # 读取 API Key（从 Streamlit secrets 读取）
    API_KEY = st.secrets["api"]["key"]
    API_URL = "https://api2.aigcbest.top/v1/chat/completions"

    # 触发生成
    if submit:
        if not user_input.strip():
            st.warning("请输入内容后再提交！")
        else:
            # 读取 Prompt 并拼接
            base_prompt = read_prompt()
            full_prompt = f"**用户输入**：\n{user_input}\n\n{base_prompt}"

            try:
                # 发送 API 请求
                response = requests.post(
                    API_URL,
                    json={"model": "gpt-4o", "messages": [{"role": "user", "content": full_prompt}]},
                    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                )

                # 解析返回结果
                data = response.json()
                reply = data["choices"][0]["message"]["content"].strip()

                # **去掉多余换行，优化行距**
                processed_text = reply.replace("，", "\n").replace("。", "\n").replace("？", "\n").replace("！", "\n").replace("：", "\n").replace("；", "\n")
                lines = [line.strip() for line in processed_text.splitlines() if line.strip()]  # 过滤空行

                # **存储到 JSON 格式的 history.txt**
                save_to_history(user_input, reply)

                # **显示诗歌**
                st.subheader("")
                st.markdown("<div class='poem-container'>", unsafe_allow_html=True)  # 诗歌整体靠右
                cols = st.columns(len(lines))  # 创建多列
                for i, line in enumerate(reversed(lines)):  # 反转顺序，使其从右到左排列
                    with cols[i]:
                        st.markdown(
                            f"<div class='poem-column {'first' if i == len(lines) - 1 else ''}'>{line}</div>",
                            unsafe_allow_html=True,
                        )
                st.markdown("</div>", unsafe_allow_html=True)  # 关闭诗歌容器

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
                file.write("")  # 清空文件内容

        # **提供下载**
        with open(HISTORY_FILE, "rb") as file:
            st.download_button(label="📥 下载历史记录 (JSON)", data=file, file_name="history.json", mime="application/json")

        # **提供清空历史的按钮**
        if st.button("🗑️ 清空历史记录"):
            os.remove(HISTORY_FILE)  # 删除文件
            with open(HISTORY_FILE, "w", encoding="utf-8") as file:
                file.write("")  # 重新创建
            st.success("✅ 历史记录已清空！")
    elif password:
        st.error("❌ 密码错误，请重试！")
