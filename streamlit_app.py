import streamlit as st
import requests

# 设置页面布局，并隐藏 Streamlit 默认 UI
st.set_page_config(page_title="深圳记忆", layout="wide")

# 使用 CSS 隐藏 Streamlit 菜单、页脚和标题栏，并居中标题和按钮
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

# **初始化 Session State**
if "poem_generated" not in st.session_state:
    st.session_state.poem_generated = False
if "poem_lines" not in st.session_state:
    st.session_state.poem_lines = []

# **仅在未生成诗歌时显示输入界面**
if not st.session_state.poem_generated:
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

                # **存储到 Session State**
                st.session_state.poem_generated = True
                st.session_state.poem_lines = lines

                # **刷新页面，使诗歌显示，输入界面隐藏**
                st.rerun()

            except Exception as e:
                st.error("请求失败，请稍后重试！")
                st.write(e)

# **如果已经生成诗歌，则仅显示诗歌**
else:
    lines = st.session_state.poem_lines

    # **使用 Streamlit columns 进行竖向排版**
    cols = st.columns(len(lines))
    for i, line in enumerate(lines):
        with cols[i]:
            text_color = "red" if i == 0 else "black"
            st.markdown(
                f"<div class='poem-column {'first' if i == 0 else ''}'>{line}</div>",
                unsafe_allow_html=True,
            )
