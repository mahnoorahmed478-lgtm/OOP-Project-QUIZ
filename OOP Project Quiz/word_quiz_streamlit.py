import streamlit as st
import random
import time
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="WORD GAME HUB", layout="centered")

# --- RESPONSIVE CSS ---
st.markdown("""
    <style>
    .main { background-color: #0a0a12; }
    
    /* Responsive Letter Boxes */
    .letter-box {
        display: inline-block;
        width: 12vw; /* Uses viewport width to scale on mobile */
        max-width: 60px;
        height: 12vw;
        max-height: 60px;
        line-height: 12vw;
        text-align: center;
        border: 2px solid #00f2ff;
        border-radius: 8px;
        margin: 4px;
        color: white;
        font-weight: bold;
        font-size: clamp(16px, 4vw, 28px); /* Adaptive font size */
        background-color: #161625;
        box-shadow: 0 4px 10px rgba(0, 242, 255, 0.3);
    }

    /* Center everything on mobile */
    .stImage, .stMarkdown, .stButton {
        display: flex;
        justify-content: center;
    }

    h1 { text-align: center; color: #ff0055; font-family: 'Impact'; font-size: clamp(30px, 10vw, 65px); }
    
    /* Improve button sizing for thumbs */
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        min-height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- WEB SOUND SYSTEM ---
# Note: Browsers block "Auto-play" sounds until the user clicks something.
# By the time a user clicks "Submit", sounds will be enabled.
def play_sound(sound_type):
    urls = {
        "success": "https://cdn.pixabay.com/audio/2022/03/15/audio_8236d9363d.mp3",
        "error": "https://cdn.pixabay.com/audio/2022/03/10/audio_c350702871.mp3"
    }
    # We use a hidden iframe to trigger the sound without refreshing
    st.components.v1.html(f"""
        <audio autoplay><source src="{urls[sound_type]}" type="audio/mpeg"></audio>
    """, height=0)

# --- DATA CLASS ---
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

# --- SESSION STATE ---
if 'init' not in st.session_state:
    st.session_state.data = LevelData()
    st.session_state.score = 0
    st.session_state.lives = 10
    st.session_state.unlocked = {"unscramble": 0, "guess_word": 0, "grid_levels": 0}
    st.session_state.screen = "MENU"
    st.session_state.input_letters = []
    st.session_state.init = True

# --- MAIN UI ---
st.markdown("<h1>WORD GAME</h1>", unsafe_allow_html=True)

if st.session_state.screen == "MENU":
    st.write("### Choose Mode")
    if st.button("1. UNSCRAMBLE WORDS"): st.session_state.screen = "LEVELS"; st.session_state.mode = "unscramble"; st.rerun()
    if st.button("2. GUESS THE WORD"): st.session_state.screen = "LEVELS"; st.session_state.mode = "guess_word"; st.rerun()
    if st.button("3. 4-IMAGE GRID QUIZ"): st.session_state.screen = "LEVELS"; st.session_state.mode = "grid_levels"; st.rerun()

elif st.session_state.screen == "LEVELS":
    mode = st.session_state.mode
    st.button("⬅ Back", on_click=lambda: st.session_state.update({"screen": "MENU"}))
    
    levels = getattr(st.session_state.data, mode)
    # Using smaller column counts for better mobile wrapping
    cols = st.columns(4) 
    for i in range(len(levels)):
        is_locked = i > st.session_state.unlocked[mode]
        label = f"{i+1}" if not is_locked else "🔒"
        if cols[i % 4].button(label, key=f"lvl_{i}", disabled=is_locked):
            st.session_state.level_idx = i
            st.session_state.screen = "PLAY"
            st.session_state.input_letters = []
            st.rerun()

elif st.session_state.screen == "PLAY":
    mode = st.session_state.mode
    level = getattr(st.session_state.data, mode)[st.session_state.level_idx]
    target = level['word']

    # Adaptive Stats Bar
    s1, s2 = st.columns(2)
    s1.metric("SCORE", st.session_state.score)
    s2.metric("LIVES", st.session_state.lives)

    if mode == "grid_levels":
        # 2x2 Image Grid
        img_cols = st.columns(2)
        for i in range(1, 5):
            name = f"{level['prefix']}{i}.png"
            path = f"OOP Project Quiz/{name}" if not os.path.exists(name) else name
            if os.path.exists(path):
                img_cols[(i-1)%2].image(path, use_container_width=True)
            else:
                img_cols[(i-1)%2].error(f"Missing: {name}")

    elif mode == "unscramble":
        if 'shuff' not in st.session_state or st.session_state.get('last_s') != st.session_state.level_idx:
            w = list(target); random.shuffle(w)
            st.session_state.shuff = "".join(w)
            st.session_state.last_s = st.session_state.level_idx
        st.markdown(f"<h2 style='text-align:center; color:#00f2ff;'>{st.session_state.shuff}</h2>", unsafe_allow_html=True)

    # --- RESPONSIVE BOXES ---
    display_html = "<div style='text-align:center; margin: 15px 0;'>"
    for i in range(len(target)):
        char = st.session_state.input_letters[i] if i < len(st.session_state.input_letters) else "&nbsp;"
        display_html += f"<div class='letter-box'>{char}</div>"
    display_html += "</div>"
    st.markdown(display_html, unsafe_allow_html=True)

    # --- LETTER BANK ---
    if 'bank' not in st.session_state or st.session_state.get('b_idx') != st.session_state.level_idx:
        b = list(target) + [random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(4)]
        random.shuffle(b)
        st.session_state.bank = b
        st.session_state.b_idx = st.session_state.level_idx

    st.write("Tap letters:")
    # 5 columns works better for mobile banks
    bank_cols = st.columns(5)
    for i, letter in enumerate(st.session_state.bank):
        if bank_cols[i % 5].button(letter, key=f"bk_{i}"):
            if len(st.session_state.input_letters) < len(target):
                st.session_state.input_letters.append(letter)
                st.rerun()

    # --- ACTION BUTTONS ---
    st.write("---")
    a1, a2 = st.columns(2)
    if a1.button("CLEAR"): st.session_state.input_letters = []; st.rerun()
    if a2.button("SUBMIT", type="primary"):
        if "".join(st.session_state.input_letters) == target:
            play_sound("success")
            st.session_state.score += 10
            st.session_state.unlocked[mode] = max(st.session_state.unlocked[mode], st.session_state.level_idx + 1)
            st.success("CORRECT!")
            time.sleep(1)
            st.session_state.screen = "LEVELS"
            st.rerun()
        else:
            play_sound("error")
            st.session_state.lives -= 1
            st.error("WRONG!")

    if st.button("HINT 💡"): st.info(f"HINT: {level['hint']}")
    st.button("⬅ QUIT", on_click=lambda: st.session_state.update({"screen": "LEVELS"}))
