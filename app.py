import streamlit as st
import time
import os
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 9: O riko'", page_icon="👕", layout="centered")

# CSS 優化
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        font-size: 24px;
        background-color: #FFD700;
        color: #333;
        border: none;
        padding: 10px;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background-color: #FFC107;
        transform: scale(1.02);
    }
    .big-font {
        font-size: 36px !important;
        font-weight: bold;
        color: #2E86C1;
        text-align: center;
        margin-bottom: 5px;
    }
    .med-font {
        font-size: 22px !important;
        color: #555;
        text-align: center;
        margin-bottom: 10px;
    }
    .card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 數據資料庫 (Unit 9 專屬) ---

# 單字：衣物 (全部小寫)
VOCABULARY = {
    "riko'":    {"zh": "衣服", "emoji": "👕", "file": "u9_riko"},
    "calao":    {"zh": "褲子", "emoji": "👖", "file": "u9_calao"},
    "cokap":    {"zh": "鞋子", "emoji": "👟", "file": "u9_cokap"},
    "topi":     {"zh": "帽子", "emoji": "🧢", "file": "u9_topi"},
    "karing":   {"zh": "眼鏡", "emoji": "👓", "file": "u9_karing"},
    "faci'":    {"zh": "包包/袋子", "emoji": "🎒", "file": "u9_faci"}
}

# 句型：動作與描述
SENTENCES = [
    {"amis": "Cica'edong to riko'.", "zh": "穿著衣服。", "file": "u9_s_wear_clothes"},
    {"amis": "Kahengangay ko topi.", "zh": "帽子是紅色的。", "file": "u9_s_red_hat"},
    {"amis": "Kohecalay ko cokap.", "zh": "鞋子是白色的。", "file": "u9_s_white_shoes"}
]

# --- 1.5 智慧語音核心 ---
def play_audio(text, filename_base=None):
    if filename_base:
        path_m4a = f"audio/{filename_base}.m4a"
        if os.path.exists(path_m4a):
            st.audio(path_m4a, format='audio/mp4')
            return
        path_mp3 = f"audio/{filename_base}.mp3"
        if os.path.exists(path_mp3):
            st.audio(path_mp3, format='audio/mp3')
            return

    try:
        # 使用印尼語 (id) 模擬南島語系發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    except:
        st.caption("🔇 (無聲)")

# --- 2. 狀態管理 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0

# --- 3. 學習模式 ---
def show_learning_mode():
    st.markdown("<h2 style='text-align: center;'>Sakasiwa: O riko'</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>我的穿搭 👕</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    words = list(VOCABULARY.items())
    
    for idx, (amis, data) in enumerate(words):
        with (col1 if idx % 2 == 0 else col2):
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <div style="font-size: 60px;">{data['emoji']}</div>
                    <div class="big-font">{amis}</div>
                    <div class="med-font">{data['zh']}</div>
                </div>
                """, unsafe_allow_html=True)
                play_audio(amis, filename_base=data.get('file'))

    st.markdown("---")
    st.markdown("### 🗣️ 句型練習")
    
    # 動作
    st.markdown("#### 👖 動作 (穿)")
    s1 = SENTENCES[0]
    st.info(f"🔹 {s1['amis']} ({s1['zh']})")
    play_audio(s1['amis'], filename_base=s1.get('file'))
    
    # 結合顏色 (Unit 8)
    st.markdown("#### 🎨 顏色描述")
    s2 = SENTENCES[1]
    st.warning(f"🔹 {s2['amis']} ({s2['zh']})")
    play_audio(s2['amis'], filename_base=s2.get('file'))

    s3 = SENTENCES[2]
    st.success(f"🔹 {s3['amis']} ({s3['zh']})")
    play_audio(s3['amis'], filename_base=s3.get('file'))

# --- 4. 測驗模式 ---
def show_quiz_mode():
    st.markdown("<h2 style='text-align: center;'>🎮 Sakasiwa 穿搭達人</h2>", unsafe_allow_html=True)
    progress = st.progress(st.session_state.current_q / 3)
    
    # 第一關：聽音辨位
    if st.session_state.current_q == 0:
        st.markdown("### 第一關：這是什麼？")
        st.write("請聽單字：")
        play_audio("cokap", filename_base="u9_cokap")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("👟 cokap (鞋子)"):
                st.balloons()
                st.success("答對了！ Cokap 是鞋子！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c2:
            if st.button("🧢 topi (帽子)"): st.error("不對喔，topi 是帽子！")

    # 第二關：句子理解 (顏色+物品)
    elif st.session_state.current_q == 1:
        st.markdown("### 第二關：哪頂帽子？")
        st.markdown("#### 請聽句子：")
        play_audio("Kahengangay ko topi.", filename_base="u9_s_red_hat")
        
        st.write("請問句子描述的是哪一個？")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🧢 紅色的帽子"):
                st.snow()
                st.success("沒錯！ Kahengangay (紅) ko topi.")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c2:
            if st.button("🧢 藍色的帽子"): st.error("不對喔，Kahengangay 是紅色！")

    # 第三關：看圖問答
    elif st.session_state.current_q == 2:
        st.markdown("### 第三關：看圖回答")
        st.markdown("#### Q: O maan koni? (這是什麼？)")
        play_audio("O maan koni?", filename_base="u9_q_what") 
        
        st.markdown("<div style='font-size:80px; text-align:center;'>👖</div>", unsafe_allow_html=True)
        
        options = ["O calao (是褲子)", "O riko' (是衣服)", "O karing (是眼鏡)"]
        choice = st.radio("請選擇：", options)
        
        if st.button("確定送出"):
            if "calao" in choice:
                st.balloons()
                st.success("太厲害了！全部答對！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.error("再看一次圖片喔！")

    else:
        st.markdown(f"<div style='text-align: center;'><h1>🏆 挑戰完成！</h1><h2>得分：{st.session_state.score}</h2></div>", unsafe_allow_html=True)
        if st.button("再玩一次"):
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.rerun()

# --- 5. 主程式入口 ---
st.sidebar.title("Unit 9: O riko' 👕")
mode = st.sidebar.radio("選擇模式", ["📖 學習單詞", "🎮 練習挑戰"])

if mode == "📖 學習單詞":
    show_learning_mode()
else:
    show_quiz_mode()
