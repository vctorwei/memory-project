import streamlit as st
import requests

st.set_page_config(page_title="记忆输入", layout="wide")

st.title("🌿 记忆输入")

# 从 Streamlit secrets 加载 API Key
API_KEY = st.secrets["api"]["key"]
API_URL = "https://api2.aigcbest.top/v1/chat/completions"

user_input = st.text_area("输入一段记忆", placeholder="请输入内容...")

if st.button("提交"):
    if not user_input.strip():
        st.warning("请输入内容后再提交！")
    else:
        prompt = f"""
        **用户输入**：{user_input}

        解析用户输入的记忆片段，并生成极简风格的诗歌。风格要求：
        - **极简主义**：短句、克制的表达、避免冗余。
        - **画面感**：以具体意象呈现情绪，而非直接表达情感。
        - **留白**：让读者自行解读诗歌背后的故事和情绪。
        - **忠于用户输入**：不额外添加复杂修辞或过多形容词。
        """

        try:
            response = requests.post(
                API_URL,
                json={"model": "gpt-4o", "messages": [{"role": "user", "content": prompt}]},
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            )

            data = response.json()
            reply = data["choices"][0]["message"]["content"].strip()

            processed_text = reply.replace("，", "\n").replace("。", "\n").replace("？", "\n").replace("！", "\n").replace("：", "\n").replace("；", "\n")
            lines = [line.strip() for line in processed_text.split("\n") if line.strip()]

            st.subheader("📖 生成的极简诗歌")
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
