import streamlit as st
import random
import time

# --- APP CONFIG ---
st.set_page_config(page_title="Word Game Hub", layout="centered")

# Custom Styling to keep your dark theme look
st.markdown("""
    <style>
    .main { background-color: #0a0a12; color: white; }
    div.stButton > button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #161625; color: white; border: 1px solid #00f2ff; font-weight: bold; }
    div.stButton > button:hover { border: 1px solid #ff0055; color: #ff0055; }
    .stat-box { background-color: #161625; padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #f1c40f; }
    </style>
    """, unsafe_allow_html=True)

# --- GAME DATA ---
if 'data' not in st.session_state:
    st.session_state.unscramble = [
        {"word": "MALL", "hint": "Women's favourite shopping spot 💅🏻."},
        {"word": "SKY", "hint": "The blue dome above us. 🌤️"},
        {"word": "CAT", "hint": "Likes to drink milk. 🐱"},
        {"word": "FISH", "hint": "Lives in water. 🐟"},
        {"word": "PYTHON", "hint": "A coding language. 🐍"},
        {"word": "LOGIC", "hint": "Reasoning behind code. 🧠"},
        {"word": "BINARY", "hint": "0s and 1s. 🔢"},
        {"word": "OBJECT", "hint": "Instance of a class. 📦"},
        {"word": "SYNTAX", "hint": "Language rules. 📝"}
    ]
    st.session_state.guess_word = [
        {"word": "LAPTOP", "hint": "A portable computer. 💻"},
        {"word": "COFFEE", "hint": "Fuel for programmers. ☕"},
        {"word": "WIFI", "hint": "Connection you can't live without. 📶"},
        {"word": "MOBILE", "hint": "Always in your hand. 📱"}
    ]

# --- INITIALIZE STATE ---
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.lives = 10
    st.session_state.unlocked = {"unscramble": 0, "guess_word": 0}
    st.session_state.current_screen = "MAIN_MENU"
    st.session_state.selected_mode = None
    st.session_state.current_level_idx = 0

# --- NAVIGATION FUNCTIONS ---
def go_to_levels(mode):
    st.session_state.selected_mode = mode
    st.session_state.current_screen = "LEVEL_SELECT"

def start_game(idx):
    st.session_state.current_level_idx = idx
    st.session_state.current_screen = "PLAYING"

# --- UI LOGIC ---
if st.session_state.current_screen == "MAIN_MENU":
    st.markdown("<h1>WORD GAME HUB</h1>", unsafe_allow_html=True)
    st.write("---")
    
    if st.button("🎮 1. UNSCRAMBLE WORDS"): go_to_levels("unscramble")
    if st.button("🧠 2. GUESS THE WORD"): go_to_levels("guess_word")
    
    st.sidebar.markdown(f"### 🏆 Score: {st.session_state.score}")
    st.sidebar.markdown(f"### ❤️ Lives: {st.session_state.lives}")

elif st.session_state.current_screen == "LEVEL_SELECT":
    mode = st.session_state.selected_mode
    st.subheader(f"{mode.replace('_', ' ').upper()} LEVELS")
    
    if st.button("⬅ Back to Menu"): st.session_state.current_screen = "MAIN_MENU"; st.rerun()

    cols = st.columns(3)
    levels = st.session_state.unscramble if mode == "unscramble" else st.session_state.guess_word
    
    for i in range(len(levels)):
        is_locked = i > st.session_state.unlocked[mode]
        btn_label = f"Level {i+1}" if not is_locked else "🔒 Locked"
        if cols[i % 3].button(btn_label, disabled=is_locked, key=f"lvl_{i}"):
            start_game(i)

elif st.session_state.current_screen == "PLAYING":
    mode = st.session_state.selected_mode
    levels = st.session_state.unscramble if mode == "unscramble" else st.session_state.guess_word
    level = levels[st.session_state.current_level_idx]

    st.write(f"### Level {st.session_state.current_level_idx + 1}")
    
    # Game Logic Display
    if mode == "unscramble":
        shuffled = list(level['word'])
        random.seed(st.session_state.current_level_idx)
        random.shuffle(shuffled)
        st.info(f"Unscramble this word: **{''.join(shuffled)}**")
    else:
        st.info("Guess the word based on the hint!")

    user_ans = st.text_input("Your Answer:", key="ans_input").upper().strip()
    
    col1, col2, col3 = st.columns([1,1,1])
    
    if col1.button("SUBMIT"):
        if user_ans == level['word']:
            st.success("Correct! 🎉")
            st.session_state.score += 10
            if st.session_state.current_level_idx == st.session_state.unlocked[mode]:
                st.session_state.unlocked[mode] += 1
            time.sleep(1)
            st.session_state.current_screen = "LEVEL_SELECT"
            st.rerun()
        else:
            st.error("Wrong! Try again.")
            st.session_state.lives -= 1

    if col2.button("HINT 💡"):
        st.warning(f"Hint: {level['hint']}")

    if col3.button("EXIT"):
        st.session_state.current_screen = "LEVEL_SELECT"
        st.rerun()