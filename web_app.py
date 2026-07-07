import streamlit as st
import csv
import json
import os
import random
from datetime import datetime, timedelta
from github import Github # 新增：用于连接 GitHub 数据库

# --- 页面配置 ---
st.set_page_config(page_title="超级背单词 云端版", page_icon="☁️", layout="centered")

TODAY_STR = datetime.now().strftime("%Y-%m-%d")

# --- 核心：连接 GitHub 云端数据库 ---
@st.cache_resource
def get_github_repo():
    # 读取我们在 Streamlit 后台配置的钥匙
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
        # 从云端读取进度
        repo = get_github_repo()
        contents = repo.get_contents("progress.json")
        return json.loads(contents.decoded_content.decode('utf-8'))
    except Exception as e:
        st.warning("首次运行或云端读取失败，已创建新存档。")
        return {
            "words_status": {}, 
            "mistakes": {},     
            "daily_stats": {"date": TODAY_STR, "new_learned": 0},
            "streak_days": 0,       
            "last_study_date": ""   
        }

def save_progress(progress_data):
    try:
        # 将进度保存回云端
        repo = get_github_repo()
        contents = repo.get_contents("progress.json")
        repo.update_file(
            contents.path, 
            "Auto update progress", 
            json.dumps(progress_data, ensure_ascii=False, indent=4), 
            contents.sha
        )
    except Exception as e:
        st.error(f"云端同步失败: {e}")

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

# 每日重置逻辑
if st.session_state.progress["daily_stats"]["date"] != TODAY_STR:
    st.session_state.progress["daily_stats"]["date"] = TODAY_STR
    st.session_state.progress["daily_stats"]["new_learned"] = 0
    save_progress(st.session_state.progress)

# --- 页面路由 ---
def go_to(page):
    st.session_state.current_page = page
    st.session_state.show_answer = False

# --- 主菜单页面 ---
def show_main_menu():
    st.title("☁️ 超级背单词 云端版")
    st.markdown(f"**🔥 连续打卡: {st.session_state.progress.get('streak_days', 0)} 天**")
    
    total_words = len(st.session_state.words_dict)
    learned_words = len(st.session_state.progress["words_status"])
    st.progress(learned_words / total_words if total_words > 0 else 0)
    st.caption(f"总词汇量掌握进度: {learned_words} / {total_words}")
    
    new_learned_today = st.session_state.progress["daily_stats"]["new_learned"]
    new_words_left = max(0, 50 - new_learned_today)
    review_list = [w for w, data in st.session_state.progress["words_status"].items() if data["next_review"] <= TODAY_STR]
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"📖 学习新词 (今日剩 {new_words_left})", use_container_width=True):
            start_quiz('learn', new_words_left)
    with col2:
        if st.button(f"🔄 每日复习 (待复习 {len(review_list)})", use_container_width=True):
            start_quiz('review', len(review_list))
            
    if st.button(f"📓 错题本 ({len(st.session_state.progress['mistakes'])})", use_container_width=True):
        go_to('mistakes')

# --- 学习逻辑 ---
def start_quiz(mode, count):
    if count <= 0:
        st.warning("这个任务已经完成啦，去看看其他的吧！")
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
        st.success(f"✅ 正确！\n\n**{current_word}** {word_info['phonetic']}\n\n{word_info['meaning']}")
    else:
        st.session_state.progress["words_status"][current_word]["interval"] = 0
        next_date = datetime.now() + timedelta(days=1)
        st.session_state.progress["words_status"][current_word]["next_review"] = next_date.strftime("%Y-%m-%d")
        
        if current_word not in st.session_state.progress["mistakes"]:
            st.session_state.progress["mistakes"][current_word] = {"count": 0, "note": ""}
        st.session_state.progress["mistakes"][current_word]["count"] += 1
        st.error(f"❌ 错误！正确答案:\n\n**{current_word}** {word_info['phonetic']}\n\n{word_info['meaning']}")

    # 答题后自动同步到云端
    with st.spinner('正在同步进度到云端...'):
        save_progress(st.session_state.progress)
        
    st.session_state.show_answer = True

# --- 答题页面 ---
def show_quiz():
    if st.session_state.quiz_index >= len(st.session_state.quiz_list):
        st.balloons()
        st.success("太棒了，你已经完成了这组单词！")
        if st.button("返回主菜单", use_container_width=True):
            go_to('main_menu')
        return

    current_word = st.session_state.quiz_list[st.session_state.quiz_index]
    word_info = st.session_state.words_dict[current_word]
    
    st.caption(f"进度: {st.session_state.quiz_index + 1} / {len(st.session_state.quiz_list)}")
    
    if st.session_state.question_type == 'en2zh':
        st.header(current_word)
        st.write("请写出它的中文意思:")
    else:
        st.header(word_info["meaning"])
        st.write("请拼写出对应的英文单词:")
        
    components_html = f"""
        <button onclick="speak()" style="padding:5px 10px; border-radius:5px; border:1px solid #ccc; background:white;">🔊 朗读</button>
        <script>
            function speak() {{
                var msg = new SpeechSynthesisUtterance('{current_word}');
                msg.lang = 'en-US';
                window.speechSynthesis.speak(msg);
            }}
        </script>
    """
    st.components.v1.html(components_html, height=40)

    if not st.session_state.show_answer:
        with st.form(key='answer_form'):
            user_input = st.text_input("你的答案:", key="user_input")
            submit_button = st.form_submit_button(label='提交答案')
            
            if submit_button:
                check_answer(user_input, current_word, word_info)
                st.rerun()
    else:
        if st.button("下一个 ➡️", use_container_width=True):
            st.session_state.quiz_index += 1
            st.session_state.question_type = random.choice(['en2zh', 'zh2en'])
            st.session_state.show_answer = False
            st.rerun()
            
    st.divider()
    if st.button("中断并返回主菜单"):
        go_to('main_menu')

# --- 错题本页面 ---
def show_mistakes():
    st.title("📓 错题本")
    mistakes = list(st.session_state.progress["mistakes"].keys())
    
    if not mistakes:
        st.success("🎉 你的错题本是空的！继续保持！")
    else:
        for word in mistakes:
            info = st.session_state.words_dict[word]
            mistake_data = st.session_state.progress["mistakes"][word]
            
            with st.expander(f"{word} (错 {mistake_data['count']} 次)"):
                st.write(f"**音标:** {info['phonetic']}")
                st.write(f"**释义:** {info['meaning']}")
                st.write(f"**笔记:** {mistake_data['note']}")
                
    st.divider()
    if st.button("返回主菜单", use_container_width=True):
        go_to('main_menu')

# --- 渲染控制 ---
if st.session_state.current_page == 'main_menu':
    show_main_menu()
elif st.session_state.current_page == 'quiz':
    show_quiz()
elif st.session_state.current_page == 'mistakes':
    show_mistakes()
