import streamlit as st
import random
import time
import os

# --- APP CONFIG ---
st.set_page_config(page_title="WORD GAME", layout="centered")

# --- CUSTOM CSS FOR BOXES & UI ---
st.markdown("""
    <style>
    .main { background-color: #0a0a12; }
    /* Letter Boxes Style */
    .letter-box {
        display: inline-block;
        width: 45px;
        height: 45px;
        line-height: 45px;
        text-align: center;
        border: 2px solid #00f2ff;
        border-radius: 5px;
        margin: 5px;
        color: white;
        font-weight: bold;
        font-size: 20px;
        background-color: #161625;
    }
    div.stButton > button {
        border-radius: 8px;
        font-weight: bold;
    }
    h1 { text-align: center; color: #ff0055; font-family: 'Impact'; }
    </style>
    """, unsafe_allow_html=True)

# --- AUDIO FUNCTION (Web Compatible) ---
def play_web_sound(sound_type):
    # Standard UI sounds using base64 or hosted URLs
    sounds = {
        "success": "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3",
        "error": "https://www.soundjay.com/buttons/sounds/button-10.mp3"
    }
    st.components.v1.html(f"""
        <audio autoplay>
            <source src="{sounds[sound_type]}" type="audio/mpeg">
        </audio>
    """, height=0)

# --- DATA ---
if 'data' not in st.session_state:
    from level_data import LevelData # Assuming you keep data in a separate file
    st.session_state.data = LevelData()
    st.session_state.score = 0
    st.session_state.lives = 10
    st.session_state.unlocked = {"unscramble": 0, "guess_word": 0, "grid_levels": 0}
    st.session_state.screen = "MENU"
    st.session_state.input_letters = []

# --- GAME LOGIC ---
st.title("WORD GAME HUB")

if st.session_state.screen == "MENU":
    if st.button("1. UNSCRAMBLE"): st.session_state.screen = "LEVELS"; st.session_state.mode = "unscramble"; st.rerun()
    if st.button("2. GUESS WORD"): st.session_state.screen = "LEVELS"; st.session_state.mode = "guess_word"; st.rerun()
    if st.button("3. 4-IMAGE GRID"): st.session_state.screen = "LEVELS"; st.session_state.mode = "grid_levels"; st.rerun()

elif st.session_state.screen == "LEVELS":
    mode = st.session_state.mode
    st.button("⬅ Back", on_click=lambda: st.session_state.update({"screen": "MENU"}))
    
    levels = getattr(st.session_state.data, mode)
    cols = st.columns(5) # 10 levels in 2 rows
    for i in range(10):
        is_locked = i > st.session_state.unlocked[mode]
        if cols[i % 5].button(f"{i+1}" if not is_locked else "🔒", key=f"l_{i}", disabled=is_locked):
            st.session_state.level_idx = i
            st.session_state.screen = "PLAY"
            st.session_state.input_letters = []
            st.rerun()

elif st.session_state.screen == "PLAY":
    mode = st.session_state.mode
    level = getattr(st.session_state.data, mode)[st.session_state.level_idx]
    
    # UI Header
    col_a, col_b = st.columns(2)
    col_a.metric("Score", st.session_state.score)
    col_b.metric("Lives", st.session_state.lives)

    # 4-IMAGE GRID SPECIFIC UI
    if mode == "grid_levels":
        # 1. Display Images
        img_cols = st.columns(2)
        for i in range(1, 5):
            img_path = f"{level['prefix']}{i}.png"
            if os.path.exists(img_path):
                img_cols[(i-1)%2].image(img_path, use_container_width=True)
            else:
                img_cols[(i-1)%2].markdown(f"<div style='height:150px; background:#222; border:1px solid #444; text-align:center; padding-top:60px;'>Image {i} Missing</div>", unsafe_allow_html=True)

        # 2. Display Result Boxes (The boxes you asked for)
        target = level['word']
        display_html = ""
        for i in range(len(target)):
            char = st.session_state.input_letters[i] if i < len(st.session_state.input_letters) else "&nbsp;"
            display_html += f"<div class='letter-box'>{char}</div>"
        st.markdown(f"<div style='text-align:center;'>{display_html}</div>", unsafe_allow_html=True)

        # 3. Letter Bank (Clickable buttons)
        st.write("### Tap Letters:")
        if 'bank' not in st.session_state or st.session_state.get('last_idx') != st.session_state.level_idx:
            bank = list(target) + [random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(4)]
            random.shuffle(bank)
            st.session_state.bank = bank
            st.session_state.last_idx = st.session_state.level_idx

        bank_cols = st.columns(6)
        for i, letter in enumerate(st.session_state.bank):
            if bank_cols[i % 6].button(letter, key=f"bank_{i}"):
                if len(st.session_state.input_letters) < len(target):
                    st.session_state.input_letters.append(letter)
                    st.rerun()

        # 4. Action Buttons
        row_btns = st.columns(3)
        if row_btns[0].button("CLEAR"): 
            st.session_state.input_letters = []
            st.rerun()
            
        if row_btns[1].button("SUBMIT", type="primary"):
            user_word = "".join(st.session_state.input_letters)
            if user_word == target:
                st.session_state.score += 10
                st.session_state.unlocked[mode] = max(st.session_state.unlocked[mode], st.session_state.level_idx + 1)
                play_web_sound("success")
                st.success("CORRECT!")
                time.sleep(1.5)
                st.session_state.screen = "LEVELS"
                st.rerun()
            else:
                play_web_sound("error")
                st.error("Wrong word!")
                st.session_state.lives -= 1

        if row_btns[2].button("HINT"):
            st.info(f"Hint: {level['hint']}")
