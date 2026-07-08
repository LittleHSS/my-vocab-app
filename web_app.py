import streamlit as st
import csv
import json
import os
import random
from datetime import datetime, timedelta
from github import Github

# --- 页面配置 ---
st.set_page_config(page_title="超级背单词", page_icon="🦉", layout="centered")

# --- 注入多邻国风格 CSS ---
st.markdown("""
<style>
    /* 全局字体和背景 */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Nunito', 'Microsoft YaHei', sans-serif;
    }
    
    /* 隐藏 Streamlit 默认的顶部菜单和底部水印 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 卡片式布局 */
    .duo-card {
        background-color: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 0px rgba(229, 229, 229, 1);
        border: 2px solid #e5e5e5;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* 统计数据大字 */
    .stat-number {
        font-size: 36px;
        font-weight: 900;
        color: #ff4b4b;
        margin: 0;
        line-height: 1;
    }
    .stat-label {
        font-size: 14px;
        color: #afafaf;
        font-weight: 700;
        text-transform: uppercase;
    }

    /* 多邻国风格立体按钮 */
    .stButton > button {
        width: 100%;
        border-radius: 16px !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        padding: 10px 24px !important;
        text-transform: uppercase;
        transition: all 0.1s ease;
        border: 2px solid #e5e5e5 !important;
        border-bottom: 4px solid #e5e5e5 !important;
        background-color: white !important;
        color: #4b4b4b !important;
    }
    
    .stButton > button:active {
        transform: translateY(2px);
        border-bottom: 2px solid #e5e5e5 !important;
    }

    /* 主动作按钮 (绿色) */
    .stButton > button[kind="primary"] {
        background-color: #58cc02 !important;
        color: white !important;
        border: 2px solid #58a700 !important;
        border-bottom: 4px solid #58a700 !important;
    }
    .stButton > button[kind="primary"]:active {
        border-bottom: 2px solid #58a700 !important;
    }
    
    /* 进度条变粗变圆 */
    .stProgress > div > div > div > div {
        background-color: #58cc02;
        border-radius: 10px;
    }
    .stProgress > div > div {
        height: 16px;
        border-radius: 10px;
        background-color: #e5e5e5;
    }
    
    /* 单词大字 */
    .huge-word {
        font-size: 48px;
        font-weight: 900;
        color: #4b4b4b;
        text-align: center;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

TODAY_STR = datetime.now().strftime("%Y-%m-%d")

# --- 核心：连接 GitHub 云端数据库 ---
@st.cache_resource
def get_github_repo():
    g = Github(st.secrets["GITHUB_TOKEN"])
    return g.get_repo(st.secrets["REPO_NAME"])

@st.cache_data
def load_words():
    words_dict = {}
    if os.path.exists('words.csv'):
        with open('words.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if not row: continue
                word = row[0].strip()
                if len(row) > 2 and row[1].strip().startswith('[') and row[2].strip().endswith(']'):
                    phonetic = row[1].strip() + "," + row[2].strip()
                    meaning = row[3].strip() if len(row) > 3 else ""
                else:
                    phonetic = row[1].strip() if len(row) > 1 else ""
                    meaning = row[2].strip() if len(row) > 2 else ""
                words_dict[word] = {"phonetic": phonetic, "meaning": meaning}
    return words_dict

def load_progress():
    try:
        repo = get_github_repo()
        contents = repo.get_contents("progress.json")
        return json.loads(contents.decoded_content.decode('utf-8'))
    except Exception as e:
        return {
            "words_status": {}, 
            "mistakes": {},     
            "daily_stats": {"date": TODAY_STR, "new_learned": 0},
            "streak_days": 0,       
            "last_study_date": ""   
        }

def save_progress(progress_data):
    try:
        repo = get_github_repo()
        contents = repo.get_contents("progress.json")
        repo.update_file(
            contents.path, 
            "Auto update progress", 
            json.dumps(progress_data, ensure_ascii=False, indent=4), 
            contents.sha
        )
    except Exception as e:
        pass

# --- 初始化 Session State ---
if 'words_dict' not in st.session_state:
    st.session_state.words_dict = load_words()
if 'progress' not in st.session_state:
    st.session_state.progress = load_progress()
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main_menu'
if 'quiz_list' not in st.session_state:
    st.session_state.quiz_list = []
if 'quiz_index' not in st.session_state:
    st.session_state.quiz_index = 0
if 'question_type' not in st.session_state:
    st.session_state.question_type = 'en2zh'
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

if st.session_state.progress["daily_stats"]["date"] != TODAY_STR:
    st.session_state.progress["daily_stats"]["date"] = TODAY_STR
    st.session_state.progress["daily_stats"]["new_learned"] = 0
    save_progress(st.session_state.progress)

def go_to(page):
    st.session_state.current_page = page
    st.session_state.show_answer = False

# --- 主菜单页面 ---
def show_main_menu():
    st.markdown("<h1 style='text-align: center; color: #58cc02;'>🦉 超级背单词</h1>", unsafe_allow_html=True)
    
    # 顶部数据卡片
    streak = st.session_state.progress.get('streak_days', 0)
    learned = len(st.session_state.progress["words_status"])
    total = len(st.session_state.words_dict)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="duo-card">
            <p class="stat-number" style="color:#ff9600;">🔥 {streak}</p>
            <p class="stat-label">连续打卡天数</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="duo-card">
            <p class="stat-number" style="color:#1cb0f6;">👑 {learned}</p>
            <p class="stat-label">已掌握词汇</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.progress(learned / total if total > 0 else 0)
    st.markdown("<br>", unsafe_allow_html=True)
    
    new_learned_today = st.session_state.progress["daily_stats"]["new_learned"]
    new_words_left = max(0, 50 - new_learned_today)
    review_list = [w for w, data in st.session_state.progress["words_status"].items() if data["next_review"] <= TODAY_STR]
    
    # 按钮区
    if st.button(f"🚀 开始学习新词 ({new_words_left})", type="primary"):
        start_quiz('learn', new_words_left)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button(f"🔄 巩固复习 ({len(review_list)})"):
            start_quiz('review', len(review_list))
    with col4:
        if st.button(f"💔 错题本 ({len(st.session_state.progress['mistakes'])})"):
            go_to('mistakes')

# --- 学习逻辑 ---
def start_quiz(mode, count):
    if count <= 0:
        st.success("任务完成！去休息一下吧。")
        return
        
    if mode == 'learn':
        unlearned = [w for w in st.session_state.words_dict.keys() if w not in st.session_state.progress["words_status"]]
        st.session_state.quiz_list = unlearned[:count]
    elif mode == 'review':
        st.session_state.quiz_list = [w for w, data in st.session_state.progress["words_status"].items() if data["next_review"] <= TODAY_STR]
        random.shuffle(st.session_state.quiz_list)
        
    st.session_state.quiz_index = 0
    st.session_state.current_mode = mode
    st.session_state.question_type = random.choice(['en2zh', 'zh2en'])
    go_to('quiz')

def update_streak():
    last_date = st.session_state.progress.get("last_study_date", "")
    if last_date != TODAY_STR:
        if last_date:
            last_date_obj = datetime.strptime(last_date, "%Y-%m-%d")
            today_obj = datetime.strptime(TODAY_STR, "%Y-%m-%d")
            if (today_obj - last_date_obj).days == 1:
                st.session_state.progress["streak_days"] = st.session_state.progress.get("streak_days", 0) + 1
            else:
                st.session_state.progress["streak_days"] = 1 
        else:
            st.session_state.progress["streak_days"] = 1
        st.session_state.progress["last_study_date"] = TODAY_STR

def check_answer(user_input, current_word, word_info):
    update_streak()
    is_correct = False
    
    if st.session_state.question_type == 'en2zh':
        if user_input and user_input in word_info["meaning"]:
            is_correct = True
    else:
        if user_input.strip().lower() == current_word.lower():
            is_correct = True

    if current_word not in st.session_state.progress["words_status"]:
        st.session_state.progress["words_status"][current_word] = {"interval": 0, "next_review": TODAY_STR}
        if st.session_state.current_mode == 'learn':
            st.session_state.progress["daily_stats"]["new_learned"] += 1

    if is_correct:
        interval = st.session_state.progress["words_status"][current_word]["interval"] + 1
        st.session_state.progress["words_status"][current_word]["interval"] = interval
        next_date = datetime.now() + timedelta(days=interval)
        st.session_state.progress["words_status"][current_word]["next_review"] = next_date.strftime("%Y-%m-%d")
        st.success(f"🎉 太棒了！\n\n**{current_word}** {word_info['phonetic']}\n\n{word_info['meaning']}")
    else:
        st.session_state.progress["words_status"][current_word]["interval"] = 0
        next_date = datetime.now() + timedelta(days=1)
        st.session_state.progress["words_status"][current_word]["next_review"] = next_date.strftime("%Y-%m-%d")
        
        if current_word not in st.session_state.progress["mistakes"]:
            st.session_state.progress["mistakes"][current_word] = {"count": 0, "note": ""}
        st.session_state.progress["mistakes"][current_word]["count"] += 1
        st.error(f"👀 差一点点！正确答案是:\n\n**{current_word}** {word_info['phonetic']}\n\n{word_info['meaning']}")

    with st.spinner('同步进度中...'):
        save_progress(st.session_state.progress)
    st.session_state.show_answer = True

# --- 答题页面 ---
def show_quiz():
    if st.session_state.quiz_index >= len(st.session_state.quiz_list):
        st.balloons()
        st.success("🎉 你完成了今天的目标！")
        if st.button("继续保持", type="primary"):
            go_to('main_menu')
        return

    current_word = st.session_state.quiz_list[st.session_state.quiz_index]
    word_info = st.session_state.words_dict[current_word]
    
    st.progress((st.session_state.quiz_index) / len(st.session_state.quiz_list))
    
    st.markdown("<div class='duo-card'>", unsafe_allow_html=True)
    if st.session_state.question_type == 'en2zh':
        st.markdown(f"<p class='huge-word'>{current_word}</p>", unsafe_allow_html=True)
        st.markdown("<p style='color:#afafaf; font-weight:bold;'>写出中文意思</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p class='huge-word'>{word_info['meaning']}</p>", unsafe_allow_html=True)
        st.markdown("<p style='color:#afafaf; font-weight:bold;'>拼写英文单词</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
        
    components_html = f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <button onclick="speak()" style="background:#1cb0f6; color:white; border:none; padding:12px 24px; border-radius:16px; font-weight:bold; font-size:16px; cursor:pointer; box-shadow: 0 4px 0 #1899d6;">
                🔊 播放发音
            </button>
        </div>
        <script>
            function speak() {{
                var msg = new SpeechSynthesisUtterance('{current_word}');
                msg.lang = 'en-US';
                window.speechSynthesis.speak(msg);
            }}
        </script>
    """
    st.components.v1.html(components_html, height=70)

    if not st.session_state.show_answer:
        with st.form(key='answer_form', clear_on_submit=True):
            user_input = st.text_input("✍️ 你的答案:", key="user_input")
            submit_button = st.form_submit_button(label='提交检查')
            
            if submit_button:
                check_answer(user_input, current_word, word_info)
                st.rerun()
    else:
        if st.button("继续 ➡️", type="primary"):
            st.session_state.quiz_index += 1
            st.session_state.question_type = random.choice(['en2zh', 'zh2en'])
            st.session_state.show_answer = False
            st.rerun()
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("结束本次练习"):
        go_to('main_menu')

# --- 错题本页面 ---
def show_mistakes():
    st.markdown("<h2 style='text-align: center; color: #ff4b4b;'>💔 错题本</h2>", unsafe_allow_html=True)
    mistakes = list(st.session_state.progress["mistakes"].keys())
    
    if not mistakes:
        st.success("🎉 你的错题本是空的！完美！")
    else:
        for word in mistakes:
            info = st.session_state.words_dict[word]
            mistake_data = st.session_state.progress["mistakes"][word]
            
            with st.expander(f"🔴 {word} (错了 {mistake_data['count']} 次)"):
                st.write(f"**音标:** {info['phonetic']}")
                st.write(f"**释义:** {info['meaning']}")
                st.write(f"**笔记:** {mistake_data['note']}")
                
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("返回主页", type="primary"):
        go_to('main_menu')

# --- 渲染控制 ---
if st.session_state.current_page == 'main_menu':
    show_main_menu()
elif st.session_state.current_page == 'quiz':
    show_quiz()
elif st.session_state.current_page == 'mistakes':
    show_mistakes()
