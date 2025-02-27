import streamlit as st
import requests
import os
import json

# 设置页面布局
st.set_page_config(page_title="深圳记忆", layout="wide", initial_sidebar_state="collapsed")

# **历史记录文件路径**
HISTORY_FILE = "history.txt"
PROMPT_FILE = "prompt.txt"

# **函数：读取 Prompt**
def read_prompt():
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    return "【错误】未找到 prompt.txt，请检查文件是否存在！"

# **UI 逻辑**
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if not st.session_state.submitted:
    # **标题**
    st.markdown(
        """
        <style>
        .title {
            font-family: SimHei, sans-serif;
            font-size: 20px;
            color: #666;
            text-align: center;
        }
        .input-container {
            display: flex;
            justify-content: center;
        }
        div[data-testid="stTextArea"] {
            width: 250px !important;
            margin: auto !important;
        }
        div[data-testid="stButton"] {
            display: flex;
            justify-content: center;
            margin-top: 10px;
        }
        </style>
        <div class='title'>关于你的深圳记忆<br>About Your Shenzhen Memory</div>
        """,
        unsafe_allow_html=True
    )
    
    # **输入框**
    user_input = st.text_area("", placeholder="输入 Type", key="memory_input")
    
    # **提交按钮**
    submit = st.button("OK")
    
    if submit and user_input.strip():
        st.session_state.submitted = True
        st.session_state.memory = user_input.strip()
        
        # **API 请求**
        API_KEY = st.secrets["api"]["key"]
        API_URL = "https://api2.aigcbest.top/v1/chat/completions"
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
            
            # 处理诗歌格式
            processed_text = reply.replace("，", "\n").replace("。", "\n").replace("？", "\n").replace("！", "\n").replace("：", "\n").replace("；", "\n")
            lines = [line.strip() for line in processed_text.splitlines() if line.strip()]
            st.session_state.poem = "\n".join(lines)
            
            # 存储
            with open(HISTORY_FILE, "a", encoding="utf-8") as file:
                file.write(json.dumps({"user_input": user_input, "generated_poem": reply}, ensure_ascii=False) + "\n")
        except Exception as e:
            st.session_state.poem = "请求失败，请稍后重试！"
else:
    # **隐藏 UI，仅显示记忆和诗歌**
    st.markdown(
        f"""
        <style>
        .memory-title {{
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            margin-top: 20vh;
        }}
        .poem-container {{
            text-align: center;
            font-size: 20px;
            margin-top: 40px;
            white-space: pre-line;
        }}
        </style>
        <div class='memory-title'>{st.session_state.memory}</div>
        <div class='poem-container'>{st.session_state.poem}</div>
        """,
        unsafe_allow_html=True
    )



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
        num_poems = min(len(poems), 10)  # 最多 10 条弹幕
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
