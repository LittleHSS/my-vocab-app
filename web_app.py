import streamlit as st
import csv
import json
import os
import random
from datetime import datetime, timedelta

# --- 页面配置 ---
st.set_page_config(page_title="新概念超级背单词", page_icon="🦉", layout="centered")

# --- 注入多邻国与现代化卡片 UI 风格 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Nunito', 'Microsoft YaHei', -apple-system, sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 卡片式容器 */
    .duo-card {
        background-color: white;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 4px 0px #e5e5e5;
        border: 2px solid #e5e5e5;
        margin-bottom: 18px;
        text-align: center;
    }
    
    .stat-number {
        font-size: 34px;
        font-weight: 900;
        margin: 0;
        line-height: 1.1;
    }
    .stat-label {
        font-size: 13px;
        color: #888888;
        font-weight: 700;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* 多邻国风格立体按钮 */
    .stButton > button {
        width: 100%;
        border-radius: 16px !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        padding: 12px 20px !important;
        transition: all 0.1s ease;
        border: 2px solid #e5e5e5 !important;
        border-bottom: 4px solid #d0d0d0 !important;
        background-color: white !important;
        color: #4b4b4b !important;
    }
    .stButton > button:active {
        transform: translateY(2px);
        border-bottom: 2px solid #e5e5e5 !important;
    }

    .stButton > button[kind="primary"] {
        background-color: #58cc02 !important;
        color: white !important;
        border: 2px solid #58a700 !important;
        border-bottom: 4px solid #488800 !important;
    }
    .stButton > button[kind="primary"]:active {
        border-bottom: 2px solid #488800 !important;
    }

    /* 选项立体按钮 (四选一) */
    .option-btn > button {
        text-align: left !important;
        justify-content: flex-start !important;
        font-size: 17px !important;
        padding: 14px 20px !important;
        margin-bottom: 8px !important;
        border-radius: 14px !important;
    }

    .stProgress > div > div > div > div {
        background-color: #58cc02;
        border-radius: 10px;
    }
    .stProgress > div > div {
        height: 14px;
        border-radius: 10px;
        background-color: #ececec;
    }
    
    .huge-word {
        font-size: 42px;
        font-weight: 900;
        color: #2b2b2b;
        text-align: center;
        margin: 15px 0 5px 0;
        letter-spacing: 0.5px;
    }
    .phonetic-tag {
        font-size: 18px;
        color: #1cb0f6;
        font-weight: 700;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

TODAY_STR = datetime.now().strftime("%Y-%m-%d")
PROGRESS_FILE = "progress.json"
WORDS_FILE = "words.csv"

# --- 1. 数据持久化层 (双保险：本地文件 + 云端GitHub自动回退) ---
def get_github_repo_safe():
    try:
        from github import Github
        if "GITHUB_TOKEN" in st.secrets and "REPO_NAME" in st.secrets:
            g = Github(st.secrets["GITHUB_TOKEN"])
            return g.get_repo(st.secrets["REPO_NAME"])
    except Exception:
        pass
    return None

def init_default_progress():
    return {
        "words_status": {}, 
        "mistakes": {},     
        "daily_stats": {"date": TODAY_STR, "new_learned": 0, "reviewed": 0},
        "streak_days": 0,       
        "last_study_date": ""   
    }

def load_progress_data():
    # 优先读本地 progress.json
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "daily_stats" not in data or data["daily_stats"].get("date") != TODAY_STR:
                    data["daily_stats"] = {"date": TODAY_STR, "new_learned": 0, "reviewed": 0}
                return data
        except Exception:
            pass

    # 若本地没有或解析失败，尝试从 GitHub 读取
    repo = get_github_repo_safe()
    if repo:
        try:
            contents = repo.get_contents(PROGRESS_FILE)
            data = json.loads(contents.decoded_content.decode("utf-8"))
            with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return data
        except Exception:
            pass

    return init_default_progress()

def save_progress_data(data):
    # 1. 立即安全保存到本地磁盘（保证刷新绝不丢失）
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.warning(f"本地保存警告: {e}")

    # 2. 尝试静默同步到 GitHub (若配置了secrets)
    repo = get_github_repo_safe()
    if repo:
        try:
            contents = repo.get_contents(PROGRESS_FILE)
            repo.update_file(
                contents.path,
                f"Auto sync: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                json.dumps(data, ensure_ascii=False, indent=4),
                contents.sha
            )
        except Exception:
            # 云端同步延迟或冲突不中断本地答题流畅度
            pass

@st.cache_data
def load_all_words():
    words_dict = {}
    if os.path.exists(WORDS_FILE):
        with open(WORDS_FILE, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            next(reader, None) # 跳过表头
            for row in reader:
                if not row or not row[0].strip(): continue
                word = row[0].strip()
                phonetic = row[1].strip() if len(row) > 1 else ""
                meaning = row[2].strip() if len(row) > 2 else ""
                words_dict[word] = {"phonetic": phonetic, "meaning": meaning}
    return words_dict

# --- 2. 初始化 Session 状态 ---
if "words_dict" not in st.session_state:
    st.session_state.words_dict = load_all_words()
if "progress" not in st.session_state:
    st.session_state.progress = load_progress_data()
if "current_page" not in st.session_state:
    st.session_state.current_page = "main_menu"
if "quiz_list" not in st.session_state:
    st.session_state.quiz_list = []
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "learn"
if "question_type" not in st.session_state:
    st.session_state.question_type = "choice"
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False
if "options" not in st.session_state:
    st.session_state.options = []
if "user_selected_idx" not in st.session_state:
    st.session_state.user_selected_idx = None
if "batch_size" not in st.session_state:
    st.session_state.batch_size = 20

def go_to(page):
    st.session_state.current_page = page
    st.session_state.show_answer = False
    st.session_state.user_selected_idx = None

def update_streak():
    prog = st.session_state.progress
    last_date = prog.get("last_study_date", "")
    if last_date != TODAY_STR:
        if last_date:
            try:
                last_dt = datetime.strptime(last_date, "%Y-%m-%d")
                curr_dt = datetime.strptime(TODAY_STR, "%Y-%m-%d")
                if (curr_dt - last_dt).days == 1:
                    prog["streak_days"] = prog.get("streak_days", 0) + 1
                elif (curr_dt - last_dt).days > 1:
                    prog["streak_days"] = 1
            except Exception:
                prog["streak_days"] = 1
        else:
            prog["streak_days"] = 1
        prog["last_study_date"] = TODAY_STR

# --- 3. 艾宾浩斯复习与出题逻辑 ---
def get_due_review_words():
    prog = st.session_state.progress
    words_status = prog.get("words_status", {})
    return [w for w, data in words_status.items() if data.get("next_review", "") <= TODAY_STR]

def get_unlearned_words():
    words_dict = st.session_state.words_dict
    words_status = st.session_state.progress.get("words_status", {})
    return [w for w in words_dict.keys() if w not in words_status]

def generate_options(target_word):
    words_dict = st.session_state.words_dict
    all_keys = list(words_dict.keys())
    if len(all_keys) < 4:
        return [target_word]
    
    distractors = random.sample([k for k in all_keys if k != target_word], 3)
    opts = distractors + [target_word]
    random.shuffle(opts)
    return opts

def start_quiz(mode, count):
    if count <= 0:
        st.toast("当前分类下没有待办单词！")
        return

    st.session_state.current_mode = mode
    if mode == "learn":
        unlearned = get_unlearned_words()
        st.session_state.quiz_list = unlearned[:count]
    elif mode == "review":
        due_words = get_due_review_words()
        random.shuffle(due_words)
        st.session_state.quiz_list = due_words[:count]
    elif mode == "mistakes":
        mistake_words = list(st.session_state.progress.get("mistakes", {}).keys())
        random.shuffle(mistake_words)
        st.session_state.quiz_list = mistake_words[:count]

    st.session_state.quiz_index = 0
    st.session_state.show_answer = False
    if st.session_state.quiz_list:
        target = st.session_state.quiz_list[0]
        st.session_state.options = generate_options(target)
    go_to("quiz")

def handle_answer_submit(is_correct, selected_idx=None):
    update_streak()
    prog = st.session_state.progress
    curr_word = st.session_state.quiz_list[st.session_state.quiz_index]
    info = st.session_state.words_dict.get(curr_word, {"phonetic": "", "meaning": ""})

    if curr_word not in prog["words_status"]:
        prog["words_status"][curr_word] = {"interval": 0, "next_review": TODAY_STR}
        prog["daily_stats"]["new_learned"] = prog["daily_stats"].get("new_learned", 0) + 1
    else:
        prog["daily_stats"]["reviewed"] = prog["daily_stats"].get("reviewed", 0) + 1

    status = prog["words_status"][curr_word]

    if is_correct:
        # 记忆成功：按照斐波那契/倍增周期推移 (1天 -> 2天 -> 4天 -> 7天 -> 15天 -> 30天)
        intervals = [1, 2, 4, 7, 15, 30, 60]
        curr_lvl = status.get("interval", 0)
        next_days = intervals[min(curr_lvl, len(intervals) - 1)]
        status["interval"] = curr_lvl + 1
        status["next_review"] = (datetime.now() + timedelta(days=next_days)).strftime("%Y-%m-%d")
        
        # 如果是错题消除，错题次数递减，归零移出错题本
        if curr_word in prog.get("mistakes", {}):
            prog["mistakes"][curr_word]["count"] -= 1
            if prog["mistakes"][curr_word]["count"] <= 0:
                del prog["mistakes"][curr_word]
    else:
        # 记错：重置周期，进入次日强制复习，加入错题本
        status["interval"] = 0
        status["next_review"] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        if "mistakes" not in prog:
            prog["mistakes"] = {}
        if curr_word not in prog["mistakes"]:
            prog["mistakes"][curr_word] = {"count": 0, "note": ""}
        prog["mistakes"][curr_word]["count"] += 1

    save_progress_data(prog)
    st.session_state.show_answer = True
    st.session_state.last_result = is_correct
    st.session_state.user_selected_idx = selected_idx

# --- 4. 页面：主菜单 (Main Menu) ---
def show_main_menu():
    st.markdown("<h1 style='text-align: center; color: #58cc02; margin-bottom: 5px;'>🦉 新概念超级背单词</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888888; font-size:14px; margin-bottom: 20px;'>第一册核心词汇 · 艾宾浩斯智能温故知新</p>", unsafe_allow_html=True)
    
    prog = st.session_state.progress
    streak = prog.get("streak_days", 0)
    learned = len(prog.get("words_status", {}))
    total = len(st.session_state.words_dict)
    due_reviews = len(get_due_review_words())
    mistakes_count = len(prog.get("mistakes", {}))
    unlearned_count = len(get_unlearned_words())

    # 顶部统计面板
    col1, col2, col3 = st.columns(3)
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
            <p class="stat-label">已学习掌握</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="duo-card">
            <p class="stat-number" style="color:#58cc02;">📚 {total}</p>
            <p class="stat-label">全书总词汇</p>
        </div>
        """, unsafe_allow_html=True)

    # 进度条
    pct = (learned / total) if total > 0 else 0
    st.progress(pct)
    st.caption(f"全书总进度: {learned} / {total} ({pct*100:.1f}%) | 今日已学新词: {prog.get('daily_stats', {}).get('new_learned', 0)}")
    st.markdown("<br>", unsafe_allow_html=True)

    # 自定义单次学习批量设置
    st.markdown("#### ⚙️ 练习设置")
    batch_opts = [10, 20, 30, 50, 100]
    st.session_state.batch_size = st.select_slider("单次学习/复习单词数量：", options=batch_opts, value=st.session_state.batch_size)
    actual_batch = st.session_state.batch_size

    st.markdown("<br>", unsafe_allow_html=True)

    # 核心动作按钮
    c_learn, c_rev = st.columns(2)
    with c_learn:
        btn_text = f"🚀 开始学新词 ({min(actual_batch, unlearned_count)} / {unlearned_count})"
        if st.button(btn_text, type="primary", disabled=(unlearned_count == 0)):
            start_quiz("learn", min(actual_batch, unlearned_count))
            st.rerun()
            
    with c_rev:
        rev_text = f"🔄 艾宾浩斯复习 ({min(actual_batch, due_reviews)} / {due_reviews})"
        if st.button(rev_text, disabled=(due_reviews == 0)):
            start_quiz("review", min(actual_batch, due_reviews))
            st.rerun()

    c_mis, c_dict = st.columns(2)
    with c_mis:
        mis_text = f"💔 错题清剿战 ({mistakes_count})"
        if st.button(mis_text, disabled=(mistakes_count == 0)):
            start_quiz("mistakes", mistakes_count)
            st.rerun()

    with c_dict:
        if st.button("📖 浏览/搜索全书词典"):
            go_to("dictionary")
            st.rerun()

# --- 5. 页面：交互式答题 (Quiz) ---
def show_quiz():
    quiz_list = st.session_state.quiz_list
    idx = st.session_state.quiz_index
    total_q = len(quiz_list)

    if idx >= total_q:
        st.balloons()
        st.markdown("""
        <div class="duo-card">
            <h2 style="color:#58cc02;">🎉 恭喜！本轮练习已全部完成！</h2>
            <p style="color:#666;">温故而知新，你的记忆又加深了一层。</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("返回主菜单 🏠", type="primary"):
            go_to("main_menu")
            st.rerun()
        return

    curr_word = quiz_list[idx]
    info = st.session_state.words_dict.get(curr_word, {"phonetic": "", "meaning": ""})
    
    # 顶部进度
    st.progress((idx) / total_q)
    st.caption(f"第 {idx + 1} / {total_q} 题 | 当前模式: {'学新词' if st.session_state.current_mode=='learn' else ('艾宾浩斯复习' if st.session_state.current_mode=='review' else '错题消灭')}")

    # 单词卡片
    st.markdown("<div class='duo-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='huge-word'>{curr_word}</div>", unsafe_allow_html=True)
    if info.get('phonetic'):
        st.markdown(f"<div class='phonetic-tag'>{info['phonetic']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 顶级真人原声发音组件 (英音 UK + 美音 US 独立双声道切换，支持自动回退)
    sound_js = f"""
    <div style="display: flex; justify-content: center; gap: 14px; margin-bottom: 20px;">
        <button id="btn_uk" onclick="playAudio('uk')" style="background:#58cc02; color:white; border:none; padding:10px 20px; border-radius:14px; font-weight:800; font-size:15px; cursor:pointer; box-shadow: 0 4px 0 #46a302; display: flex; align-items: center; gap: 6px;">
            🇬🇧 英音发音
        </button>
        <button id="btn_us" onclick="playAudio('us')" style="background:#1cb0f6; color:white; border:none; padding:10px 20px; border-radius:14px; font-weight:800; font-size:15px; cursor:pointer; box-shadow: 0 4px 0 #1899d6; display: flex; align-items: center; gap: 6px;">
            🇺🇸 美音发音
        </button>
    </div>
    <audio id="audio_player" style="display:none;"></audio>
    <script>
        var rawWord = encodeURIComponent("{curr_word.strip().lower()}");
        
        function playAudio(accent) {{
            var typeVal = (accent === 'uk') ? '1' : '2';
            var audioUrl = "https://dict.youdao.com/dictvoice?type=" + typeVal + "&audio=" + rawWord;
            var player = document.getElementById("audio_player");
            
            player.src = audioUrl;
            var playPromise = player.play();
            
            if (playPromise !== undefined) {{
                playPromise.catch(function(error) {{
                    // 若网络受限或无法加载，平滑回退到浏览器本地高保真合成发音
                    var fallbackLang = (accent === 'uk') ? 'en-GB' : 'en-US';
                    var msg = new SpeechSynthesisUtterance("{curr_word}");
                    msg.lang = fallbackLang;
                    msg.rate = 0.85;
                    window.speechSynthesis.speak(msg);
                }});
            }}
        }}

        // 默认载入时轻声播放英音（新概念传统英音）
        window.onload = function() {{
            setTimeout(function() {{ playAudio('uk'); }}, 200);
        }};
    </script>
    """
    st.components.v1.html(sound_js, height=65)

    # 四选一单选面板
    if not st.session_state.show_answer:
        st.markdown("<p style='text-align:center; color:#888; font-weight:bold;'>👉 请选出对应的中文释义：</p>", unsafe_allow_html=True)
        for i, opt in enumerate(st.session_state.options):
            opt_meaning = st.session_state.words_dict.get(opt, {}).get("meaning", opt)
            if st.button(f"{chr(65+i)}.  {opt_meaning}", key=f"opt_{idx}_{i}"):
                is_correct = (opt == curr_word)
                handle_answer_submit(is_correct, selected_idx=i)
                st.rerun()
    else:
        # 显示答题结果与详尽解析
        if st.session_state.last_result:
            st.success(f"🎯 **太棒了！回答正确！**\n\n**{curr_word}** {info['phonetic']}\n\n**释义:** {info['meaning']}")
        else:
            st.error(f"❌ **差一点点！正确答案是：**\n\n**{curr_word}** {info['phonetic']}\n\n**释义:** {info['meaning']}\n\n*(已自动加入错题本，稍后将强化复习)*")

        if st.button("下一个单词 ➡️", type="primary"):
            st.session_state.quiz_index += 1
            st.session_state.show_answer = False
            st.session_state.user_selected_idx = None
            if st.session_state.quiz_index < len(quiz_list):
                next_word = quiz_list[st.session_state.quiz_index]
                st.session_state.options = generate_options(next_word)
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("暂停并返回主页 ⏸️"):
        go_to("main_menu")
        st.rerun()

# --- 6. 页面：全书词典与搜索 (Dictionary) ---
def show_dictionary():
    st.markdown("<h2 style='text-align:center; color:#1cb0f6;'>📖 新概念第一册完整词库</h2>", unsafe_allow_html=True)
    
    words_dict = st.session_state.words_dict
    prog = st.session_state.progress
    words_status = prog.get("words_status", {})

    search_query = st.text_input("🔍 搜索单词或中文释义 (支持中英文关键词):", "").strip().lower()

    filtered_words = []
    for w, info in words_dict.items():
        if not search_query or search_query in w.lower() or search_query in info["meaning"].lower():
            filtered_words.append((w, info))

    st.caption(f"共找到 {len(filtered_words)} 个词汇")

    # 列表展示 (分页或截取前 100 项防止卡顿)
    for w, info in filtered_words[:100]:
        status_tag = "👑 已学" if w in words_status else "⚪ 未学"
        with st.expander(f"{w}  |  {info['phonetic']}  |  {status_tag}"):
            st.write(f"**中文释义:** {info['meaning']}")
            if w in words_status:
                st.write(f"**记忆周期级别:** Lvl {words_status[w].get('interval', 0)}")
                st.write(f"**下次复习日期:** {words_status[w].get('next_review', '')}")

    if len(filtered_words) > 100:
        st.info("💡 为保证页面流畅，已展示前 100 条结果，请输入更精确的关键词搜索。")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("返回主菜单 🏠", type="primary"):
        go_to("main_menu")
        st.rerun()

# --- 7. 页面路由调度 ---
if st.session_state.current_page == "main_menu":
    show_main_menu()
elif st.session_state.current_page == "quiz":
    show_quiz()
elif st.session_state.current_page == "dictionary":
    show_dictionary()
