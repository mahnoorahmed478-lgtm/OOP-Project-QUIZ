import streamlit as st
import random
import time
import os
from PIL import Image

# --- STYLING ---
st.set_page_config(page_title="WORD GAME", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0a0a12; }
    div.stButton > button { 
        width: 100%; border-radius: 5px; height: 3.5em; 
        background-color: #161625; color: white; 
        border: 1px solid #00f2ff; font-weight: bold;
    }
    div.stButton > button:hover { border: 1px solid #ff0055; color: #ff0055; }
    h1 { text-align: center; color: #ff0055; font-family: 'Impact'; font-size: 70px; }
    .status-text { color: #f1c40f; font-weight: bold; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- ORIGINAL DATA CLASS ---
class LevelData:
    def __init__(self):
        self.unscramble = [
            {"word": "MALL", "hint": "Women's favourite shopping spot 💅🏻."},
            {"word": "SKY", "hint": "The blue dome above us. 🌤️"},
            {"word": "CAT", "hint": "Likes to drink milk. 🐱"},
            {"word": "FISH", "hint": "Lives in water. 🐟"},
            {"word": "FUTURE", "hint": "It is a tense and dark for us students. 😶‍🌫️"},
            {"word": "PYTHON", "hint": "A coding language. 🐍"},
            {"word": "LOGIC", "hint": "Reasoning behind code. 🧠"},
            {"word": "BINARY", "hint": "0s and 1s. 🔢"},
            {"word": "OBJECT", "hint": "Instance of a class. 📦"},
            {"word": "SYNTAX", "hint": "Language rules. 📝"}
        ]
        self.guess_word = [
            {"word": "LAPTOP", "hint": "A portable computer. 💻"},
            {"word": "COFFEE", "hint": "Fuel for programmers. ☕"},
            {"word": "WIFI", "hint": "Connection you can't live without. 📶"},
            {"word": "MOBILE", "hint": "Always in your hand. 📱"},
            {"word": "KEYBOARD", "hint": "Used for typing code. ⌨️"},
            {"word": "MOUSE", "hint": "Used to click and scroll. 🖱️"},
            {"word": "BROWSER", "hint": "Chrome, Safari, or Edge. 🌐"},
            {"word": "PIXELS", "hint": "Tiny dots on your screen. 🖼️"},
            {"word": "CAMERA", "hint": "Used for video calls. 📷"},
            {"word": "SCREEN", "hint": "Where you see the output. 🖥️"}
        ]
        self.grid_levels = [
            {"word": "LEAF", "hint": "Green part of a plant.", "prefix": "leaf"},
            {"word": "HIDE", "hint": "Keep out of sight.", "prefix": "hide"},
            {"word": "COLD", "hint": "Low temperature. ❄️", "prefix": "cold"},
            {"word": "BURN", "hint": "Hot and burning. 🔥", "prefix": "burn"},
            {"word": "DROP", "hint": "Water falling from clouds. 🌧️", "prefix": "drop"},
            {"word": "DUSK", "hint": "Time just before dark. 🌇", "prefix": "dusk"},
            {"word": "MIST", "hint": "Tiny water droplets in air. ☁️", "prefix": "mist"},
            {"word": "HAZE", "hint": "Atmospheric obscurity. 🌪️", "prefix": "haze"},
            {"word": "TORN", "hint": "Ripped or damaged.", "prefix": "torn"},
            {"word": "GLOW", "hint": "Soft light.", "prefix": "glow"}
        ]

# --- INITIALIZATION ---
if 'initialized' not in st.session_state:
    st.session_state.data = LevelData()
    st.session_state.score = 0
    st.session_state.lives = 10
    st.session_state.unlocked = {"unscramble": 0, "guess_word": 0, "grid_levels": 0}
    st.session_state.screen = "MAIN_MENU"
    st.session_state.mode = None
    st.session_state.level_idx = 0
    st.session_state.initialized = True

# --- SCREEN CONTROLLERS ---
def change_screen(new_screen, mode=None):
    st.session_state.screen = new_screen
    if mode: st.session_state.mode = mode
    st.rerun()

# --- UI DISPLAY ---
st.markdown("<h1>WORD GAME</h1>", unsafe_allow_html=True)

# Sidebar Stats
st.sidebar.markdown(f"<p class='status-text'>❤️ LIVES: {st.session_state.lives}</p>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p class='status-text'>🏆 SCORE: {st.session_state.score}</p>", unsafe_allow_html=True)

if st.session_state.screen == "MAIN_MENU":
    st.write("### Choose Your Mode")
    if st.button("1. UNSCRAMBLE WORDS"): change_screen("LEVEL_SELECT", "unscramble")
    if st.button("2. GUESS THE WORD"): change_screen("LEVEL_SELECT", "guess_word")
    if st.button("3. 4-IMAGE GRID QUIZ"): change_screen("LEVEL_SELECT", "grid_levels")

elif st.session_state.screen == "LEVEL_SELECT":
    mode = st.session_state.mode
    st.write(f"### {mode.upper()} - Select Level")
    if st.button("⬅ BACK TO MENU"): change_screen("MAIN_MENU")
    
    levels = getattr(st.session_state.data, mode)
    cols = st.columns(3)
    for i in range(len(levels)):
        is_locked = i > st.session_state.unlocked[mode]
        
        if i < 4: d_text = "EASY"
        elif i < 7: d_text = "MEDIUM"
        else: d_text = "HARD"
        
        label = f"Level {i+1}\n({d_text})" if not is_locked else f"Level {i+1} 🔒"
        if cols[i % 3].button(label, disabled=is_locked, key=f"lvl_{i}"):
            st.session_state.level_idx = i
            st.session_state.screen = "PLAYING"
            st.rerun()

elif st.session_state.screen == "PLAYING":
    mode = st.session_state.mode
    levels = getattr(st.session_state.data, mode)
    current_level = levels[st.session_state.level_idx]
    
    if st.button("⬅ BACK TO LEVELS"): change_screen("LEVEL_SELECT")

    # Game UI
    if mode == "grid_levels":
        cols = st.columns(2)
        for i in range(1, 5):
            path = f"{current_level['prefix']}{i}.png"
            if os.path.exists(path):
                cols[(i-1)%2].image(path, use_container_width=True)
            else:
                cols[(i-1)%2].warning(f"Image {i} missing")
    
    elif mode == "unscramble":
        word = current_level['word']
        shuffled = "".join(random.sample(word, len(word)))
        st.markdown(f"<h2 style='text-align:center; color:#00f2ff;'>{shuffled}</h2>", unsafe_allow_html=True)
    
    st.write("---")
    ans = st.text_input("ENTER WORD:", key="game_input").upper().strip()
    
    c1, c2 = st.columns(2)
    if c1.button("SUBMIT"):
        if ans == current_level['word']:
            st.balloons()
            st.session_state.score += 10
            if st.session_state.level_idx == st.session_state.unlocked[mode]:
                st.session_state.unlocked[mode] += 1
            st.success("WELL DONE!")
            time.sleep(2)
            change_screen("LEVEL_SELECT")
        else:
            st.error("WRONG ANSWER! TRY AGAIN")
            st.session_state.lives -= 1

    if c2.button("HINT"):
        st.info(f"💡 Hint: {current_level['hint']}")
