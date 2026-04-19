import streamlit as st
import random
import time
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="WORD GAME HUB", layout="centered")

# --- CUSTOM CSS FOR PERFECT ALIGNMENT ---
st.markdown("""
    <style>
    .main { background-color: #0a0a12; }
    
    /* Image Grid Container */
    .image-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-bottom: 20px;
    }
    .game-img {
        width: 100%;
        aspect-ratio: 1 / 1;
        object-fit: cover;
        border-radius: 10px;
        border: 1px solid #333;
    }

    /* Magnetic Letter Boxes */
    .letter-area {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 8px;
        margin: 20px 0;
    }
    .letter-box {
        width: 50px;
        height: 50px;
        line-height: 50px;
        text-align: center;
        border: 2px solid #00f2ff;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        font-size: 24px;
        background-color: #161625;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
    }

    /* Mobile Responsive Tweaks */
    @media (max-width: 600px) {
        .letter-box { width: 40px; height: 40px; line-height: 40px; font-size: 18px; }
        h1 { font-size: 40px !important; }
    }

    h1 { text-align: center; color: #ff0055; font-family: 'Impact'; font-size: 60px; }
    div.stButton > button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SOUND SYSTEM ---
def play_sound(sound_type):
    urls = {
        "success": "https://cdn.pixabay.com/audio/2022/03/15/audio_8236d9363d.mp3",
        "error": "https://cdn.pixabay.com/audio/2022/03/10/audio_c350702871.mp3"
    }
    st.components.v1.html(f"""
        <audio autoplay><source src="{urls[sound_type]}" type="audio/mpeg"></audio>
        <script>document.querySelector('audio').volume = 0.5;</script>
    """, height=0)

# --- DATA CLASS ---
class LevelData:
    def __init__(self):
        self.unscramble = [
            {"word": "MALL", "hint": "Shopping spot 💅🏻."}, {"word": "SKY", "hint": "Blue dome 🌤️"},
            {"word": "CAT", "hint": "Drinks milk 🐱"}, {"word": "FISH", "hint": "Lives in water 🐟"},
            {"word": "FUTURE", "hint": "Tense for students 😶‍🌫️"}, {"word": "PYTHON", "hint": "Coding language 🐍"},
            {"word": "LOGIC", "hint": "Code reasoning 🧠"}, {"word": "BINARY", "hint": "0s and 1s 🔢"},
            {"word": "OBJECT", "hint": "Class instance 📦"}, {"word": "SYNTAX", "hint": "Language rules 📝"}
        ]
        self.guess_word = [
            {"word": "LAPTOP", "hint": "Portable computer 💻"}, {"word": "COFFEE", "hint": "Programmer fuel ☕"},
            {"word": "WIFI", "hint": "Essential connection 📶"}, {"word": "MOBILE", "hint": "In your hand 📱"},
            {"word": "KEYBOARD", "hint": "Typing tool ⌨️"}, {"word": "MOUSE", "hint": "Click and scroll 🖱️"},
            {"word": "BROWSER", "hint": "Web access 🌐"}, {"word": "PIXELS", "hint": "Screen dots 🖼️"},
            {"word": "CAMERA", "hint": "Video calls 📷"}, {"word": "SCREEN", "hint": "Output display 🖥️"}
        ]
        self.grid_levels = [
            {"word": "LEAF", "hint": "Plant part", "prefix": "leaf"}, {"word": "HIDE", "hint": "Stay unseen", "prefix": "hide"},
            {"word": "COLD", "hint": "Low temp ❄️", "prefix": "cold"}, {"word": "BURN", "hint": "Hot 🔥", "prefix": "burn"},
            {"word": "DROP", "hint": "Rain falling 🌧️", "prefix": "drop"}, {"word": "DUSK", "hint": "Before dark 🌇", "prefix": "dusk"},
            {"word": "MIST", "hint": "Water in air ☁️", "prefix": "mist"}, {"word": "HAZE", "hint": "🌪️", "prefix": "haze"},
            {"word": "TORN", "hint": "Ripped", "prefix": "torn"}, {"word": "GLOW", "hint": "Soft light", "prefix": "glow"}
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
    if st.button("1. UNSCRAMBLE"): st.session_state.screen = "LEVELS"; st.session_state.mode = "unscramble"; st.rerun()
    if st.button("2. GUESS WORD"): st.session_state.screen = "LEVELS"; st.session_state.mode = "guess_word"; st.rerun()
    if st.button("3. 4-IMAGE GRID"): st.session_state.screen = "LEVELS"; st.session_state.mode = "grid_levels"; st.rerun()

elif st.session_state.screen == "LEVELS":
    mode = st.session_state.mode
    st.button("⬅ Back", on_click=lambda: st.session_state.update({"screen": "MENU"}))
    levels = getattr(st.session_state.data, mode)
    cols = st.columns(5)
    for i in range(len(levels)):
        is_locked = i > st.session_state.unlocked[mode]
        if cols[i % 5].button(f"{i+1}" if not is_locked else "🔒", key=f"l_{i}", disabled=is_locked):
            st.session_state.level_idx = i
            st.session_state.screen = "PLAY"
            st.session_state.input_letters = []
            st.rerun()

elif st.session_state.screen == "PLAY":
    mode = st.session_state.mode
    level = getattr(st.session_state.data, mode)[st.session_state.level_idx]
    target = level['word']

    # Stats Bar
    s1, s2 = st.columns(2)
    s1.metric("SCORE", st.session_state.score)
    s2.metric("LIVES", st.session_state.lives)

    if mode == "grid_levels":
        # Pure HTML/CSS for perfect image alignment
        img_html = '<div class="image-container">'
        for i in range(1, 5):
            name = f"{level['prefix']}{i}.png"
            # Attempt to find the file in root or Project folder
            path = name if os.path.exists(name) else f"OOP Project Quiz/{name}"
            img_html += f'<img src="data:image/png;base64,...">' if not os.path.exists(path) else "" 
            # Note: For best results, Streamlit's st.image is safer for local files
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        for i in range(1, 5):
            name = f"{level['prefix']}{i}.png"
            path = name if os.path.exists(name) else f"OOP Project Quiz/{name}"
            (c1 if i % 2 != 0 else c2).image(path if os.path.exists(path) else "https://via.placeholder.com/150", use_container_width=True)

    elif mode == "unscramble":
        if 'sh' not in st.session_state or st.session_state.get('li') != st.session_state.level_idx:
            w = list(target); random.shuffle(w)
            st.session_state.sh = "".join(w); st.session_state.li = st.session_state.level_idx
        st.markdown(f"<h2 style='text-align:center; color:#00f2ff;'>{st.session_state.sh}</h2>", unsafe_allow_html=True)

    # --- THE BOXES ---
    box_html = '<div class="letter-area">'
    for i in range(len(target)):
        char = st.session_state.input_letters[i] if i < len(st.session_state.input_letters) else "&nbsp;"
        box_html += f'<div class="letter-box">{char}</div>'
    st.markdown(box_html + '</div>', unsafe_allow_html=True)

    # --- LETTER BANK ---
    if 'bank' not in st.session_state or st.session_state.get('bi') != st.session_state.level_idx:
        b = list(target) + [random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(4)]
        random.shuffle(b); st.session_state.bank = b; st.session_state.bi = st.session_state.level_idx

    st.write("Tap letters:")
    bank_cols = st.columns(6)
    for i, letter in enumerate(st.session_state.bank):
        if bank_cols[i % 6].button(letter, key=f"bk_{i}"):
            if len(st.session_state.input_letters) < len(target):
                st.session_state.input_letters.append(letter)
                st.rerun()

    # --- ACTIONS ---
    st.write("---")
    a1, a2, a3 = st.columns(3)
    if a1.button("CLEAR"): st.session_state.input_letters = []; st.rerun()
    if a2.button("SUBMIT", type="primary"):
        if "".join(st.session_state.input_letters) == target:
            play_sound("success")
            st.session_state.score += 10
            st.session_state.unlocked[mode] = max(st.session_state.unlocked[mode], st.session_state.level_idx + 1)
            st.success("CORRECT!")
            time.sleep(1); st.session_state.screen = "LEVELS"; st.rerun()
        else:
            play_sound("error")
            st.session_state.lives -= 1; st.error("WRONG!")

    if a3.button("HINT 💡"): st.info(f"HINT: {level['hint']}")
    st.button("⬅ QUIT", on_click=lambda: st.session_state.update({"screen": "LEVELS"}))
