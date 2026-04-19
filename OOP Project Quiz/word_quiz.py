import tkinter as tk
from tkinter import messagebox
import random
import winsound
import os

# Fail-safe PIL import
try:
    from PIL import Image, ImageTk
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

# --- COLORS ---
C_BG = "#0a0a12"
C_CARD = "#161625"
C_ACCENT = "#00f2ff"
C_PINK = "#ff0055"
C_GOLD = "#f1c40f"
C_SILVER = "#bdc3c7"
C_BRONZE = "#cd7f32"
C_EASY = "#27ae60"
C_MEDIUM = "#f39c12"
C_HARD = "#e74c3c"

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

class WordQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WORD GAME") 
        self.root.geometry("650x900")
        self.root.configure(bg=C_BG)

        self.data = LevelData()
        self.score = 0
        self.lives = 10 
        self.level_idx = 0
        self.current_mode = ""
        self.user_input_var = tk.StringVar()
        self.user_input_letters = [] 
        self.trace_id = None
        self.unlocked_levels = {"unscramble": 0, "guess_word": 0, "grid_levels": 0}
        
        self.main_menu()

    def clear_screen(self):
        if self.trace_id:
            try: self.user_input_var.trace_remove("write", self.trace_id)
            except: pass
            self.trace_id = None
        for widget in self.root.winfo_children():
            widget.destroy()

    def play_sound(self, s_type):
        try:
            if s_type == "success": winsound.Beep(1000, 150)
            elif s_type == "medal": winsound.Beep(1500, 500)
            elif s_type == "error": winsound.Beep(400, 300)
            elif s_type == "click": winsound.Beep(1200, 80)
            elif s_type == "pop": winsound.Beep(700, 40)
        except: pass

    def main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="WORD GAME", font=("Impact", 75), fg=C_PINK, bg=C_BG).pack(pady=80)
        
        modes = [
            ("1. UNSCRAMBLE WORDS", "unscramble"),
            ("2. GUESS THE WORD", "guess_word"),
            ("3. 4-IMAGE GRID QUIZ", "grid_levels")
        ]

        for text, mode in modes:
            btn = tk.Button(self.root, text=text, font=("Arial", 14, "bold"), width=30, height=2,
                            bg=C_CARD, fg="white", relief="flat", cursor="hand2",
                            command=lambda m=mode: [self.play_sound("click"), self.show_level_selection(m)])
            btn.pack(pady=12)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=C_ACCENT, fg=C_BG))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=C_CARD, fg="white"))

    def show_level_selection(self, mode):
        self.clear_screen()
        self.current_mode = mode
        
        header = tk.Frame(self.root, bg=C_BG)
        header.pack(fill="x", padx=20, pady=20)
        tk.Button(header, text="⬅ BACK", font=("Arial", 10, "bold"), bg=C_CARD, fg="white", 
                  relief="flat", command=self.main_menu).pack(side="left")
        tk.Label(header, text=mode.replace("_", " ").upper(), font=("Arial", 18, "bold"), fg=C_GOLD, bg=C_BG).pack(side="right")

        grid_frame = tk.Frame(self.root, bg=C_BG)
        grid_frame.pack(pady=20)

        for i in range(10):
            if i < 4: d_text, d_col = "EASY", C_EASY
            elif i < 7: d_text, d_col = "MEDIUM", C_MEDIUM
            else: d_text, d_col = "HARD", C_HARD

            is_locked = i > self.unlocked_levels[mode]
            btn_txt = f"Level {i+1}\n{d_text}" if not is_locked else f"Level {i+1}\n🔒"
            btn_bg = d_col if not is_locked else "#2a2a35"
            
            btn = tk.Button(grid_frame, text=btn_txt, font=("Arial", 10, "bold"), width=14, height=4, 
                            bg=btn_bg, fg="white", relief="flat",
                            command=lambda idx=i, L=is_locked: self.start_level(idx) if not L else None)
            btn.grid(row=i//3, column=i%3, padx=8, pady=8)

    def start_level(self, idx):
        self.level_idx = idx
        self.load_game_ui()

    def load_game_ui(self):
        self.clear_screen()
        self.user_input_letters = []
        self.user_input_var.set("")
        
        stats = tk.Frame(self.root, bg=C_CARD, pady=10)
        stats.pack(fill="x")
        self.life_lbl = tk.Label(stats, text=f"LIVES: {self.lives} ❤️", fg=C_PINK, bg=C_CARD, font=("Arial", 14, "bold"))
        self.life_lbl.pack(side="left", padx=20)
        tk.Label(stats, text=f"SCORE: {self.score}", fg=C_GOLD, bg=C_CARD, font=("Arial", 14, "bold")).pack(side="right", padx=20)

        level_list = getattr(self.data, self.current_mode)
        level = level_list[self.level_idx]

        if self.current_mode == "grid_levels":
            self.setup_grid_ui(level)
        else:
            if self.current_mode == "unscramble":
                shuffled = "".join(random.sample(level['word'], len(level['word'])))
                tk.Label(self.root, text=shuffled, font=("Courier", 55, "bold"), fg=C_ACCENT, bg=C_BG).pack(pady=40)
            self.setup_typing_ui(level)

    def setup_typing_ui(self, level):
        self.word_display = tk.Label(self.root, text="_ " * len(level['word']), font=("Courier", 45, "bold"), fg="white", bg=C_BG)
        self.word_display.pack(pady=30)
        self.entry = tk.Entry(self.root, textvariable=self.user_input_var, font=("Arial", 28), justify="center", bg=C_CARD, fg=C_ACCENT, insertbackground="white", relief="flat", highlightthickness=2, highlightbackground=C_CARD)
        self.entry.pack(pady=20, padx=80, fill="x")
        self.entry.focus_set()
        self.trace_id = self.user_input_var.trace_add("write", lambda *a: self.sync_blanks(level['word']))
        self.create_action_btns(level)

    def setup_grid_ui(self, level):
        grid = tk.Frame(self.root, bg=C_BG)
        grid.pack(pady=10)
        for i in range(1, 5):
            path = f"{level['prefix']}{i}.png"
            lbl = tk.Label(grid, width=18, height=8, bg=C_CARD, relief="solid", highlightthickness=2, highlightbackground=C_ACCENT)
            if HAS_PILLOW and os.path.exists(path):
                img = Image.open(path).resize((150, 150))
                photo = ImageTk.PhotoImage(img)
                lbl.config(image=photo)
                lbl.image = photo 
            else: lbl.config(text=f"IMG {i}", fg="gray")
            lbl.grid(row=(i-1)//2, column=(i-1)%2, padx=10, pady=10)

        self.word_display = tk.Label(self.root, text="_ " * len(level['word']), font=("Courier", 35, "bold"), fg="white", bg=C_BG)
        self.word_display.pack(pady=15)
        
        bank = tk.Frame(self.root, bg=C_BG)
        bank.pack(pady=10)
        pool = list(level['word']) + [random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(4)]
        random.shuffle(pool)
        for i, char in enumerate(pool):
            tk.Button(bank, text=char, width=5, height=2, font=("Arial", 12, "bold"), bg=C_CARD, fg="white", relief="flat", command=lambda c=char: self.handle_grid_click(c, level['word'])).grid(row=i//6, column=i%6, padx=5, pady=5)
        self.create_action_btns(level, is_grid=True)

    def sync_blanks(self, target):
        typed = self.user_input_var.get().upper()
        if len(typed) > len(target): self.user_input_var.set(typed[:len(target)])
        display = [typed[i] if i < len(typed) else "_" for i in range(len(target))]
        self.word_display.config(text=" ".join(display))
        if typed: self.play_sound("pop")

    def handle_grid_click(self, char, correct):
        if len(self.user_input_letters) < len(correct):
            self.play_sound("pop")
            self.user_input_letters.append(char)
            display = " ".join(self.user_input_letters) + " _" * (len(correct) - len(self.user_input_letters))
            self.word_display.config(text=display)

    def create_action_btns(self, level, is_grid=False):
        self.err_lbl = tk.Label(self.root, text="", font=("Arial", 14, "bold"), fg=C_PINK, bg=C_BG)
        self.err_lbl.pack(pady=5)
        self.hint_lbl = tk.Label(self.root, text="", font=("Arial", 12, "italic"), fg=C_GOLD, bg=C_BG)
        self.hint_lbl.pack(pady=5)
        btns = tk.Frame(self.root, bg=C_BG)
        btns.pack(pady=10)
        tk.Button(btns, text="SUBMIT", bg="#27ae60", fg="white", font=("Arial", 12, "bold"), width=15, height=2, relief="flat", command=lambda: self.check(level['word'], is_grid)).grid(row=0, column=0, padx=10)
        tk.Button(btns, text="HINT (❤️-1)", bg=C_GOLD, fg=C_BG, font=("Arial", 12, "bold"), width=15, height=2, relief="flat", command=lambda: self.trigger_hint(level['hint'])).grid(row=0, column=1, padx=10)

    def trigger_hint(self, hint):
        if self.lives > 0:
            self.lives -= 1
            self.play_sound("click")
            self.life_lbl.config(text=f"LIVES: {self.lives} ❤️")
            self.hint_lbl.config(text=f"HINT: {hint}")
        else: messagebox.showwarning("OUT OF LIVES", "No lives left for hints!")

    def check(self, correct, is_grid):
        val = "".join(self.user_input_letters).upper() if is_grid else self.user_input_var.get().upper().strip()
        if val == correct:
            self.play_sound("success")
            self.score += 10
            # Milestone logic
            level_num = self.level_idx + 1
            
            # Unlock next level
            if self.level_idx == self.unlocked_levels[self.current_mode]:
                self.unlocked_levels[self.current_mode] += 1
            
            if level_num == 4: self.show_medal("BRONZE", C_BRONZE)
            elif level_num == 7: self.show_medal("SILVER", C_SILVER)
            elif level_num == 10: self.show_medal("GOLD", C_GOLD, final=True)
            else: self.show_win()
        else:
            self.play_sound("error")
            self.err_lbl.config(text="ERRRR! WRONG ANSWER")
            if not is_grid: self.entry.config(highlightbackground=C_PINK)
            self.root.after(1000, lambda: [self.err_lbl.config(text=""), self.reset_ui(is_grid, len(correct))])

    def reset_ui(self, is_grid, length):
        if is_grid:
            self.user_input_letters = []
            self.word_display.config(text="_ " * length)
        else:
            self.entry.config(highlightbackground=C_CARD)
            self.user_input_var.set("")

    def show_win(self):
        self.clear_screen()
        tk.Label(self.root, text="WELL DONE!", font=("Impact", 80), fg=C_ACCENT, bg=C_BG).pack(expand=True)
        self.root.after(1200, lambda: self.show_level_selection(self.current_mode))

    def show_medal(self, medal_type, color, final=False):
        self.clear_screen()
        self.play_sound("medal")
        
        frame = tk.Frame(self.root, bg=C_BG)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(frame, text="VICTORY", font=("Impact", 40), fg="white", bg=C_BG).pack()
        tk.Label(frame, text=f"{medal_type} MEDAL", font=("Impact", 60), fg=color, bg=C_BG).pack(pady=20)
        
        # Medal Icon (Text-based emoji/shape)
        tk.Label(frame, text="🏅", font=("Arial", 100), bg=C_BG, fg=color).pack()
        
        if final:
            tk.Button(frame, text="RETURN TO MAIN MENU", font=("Arial", 14, "bold"), bg=C_ACCENT, fg=C_BG, 
                      padx=20, pady=10, relief="flat", command=self.main_menu).pack(pady=40)
        else:
            tk.Label(frame, text="Advancing to Next Tier...", font=("Arial", 12), fg="gray", bg=C_BG).pack(pady=20)
            self.root.after(3000, lambda: self.show_level_selection(self.current_mode))

if __name__ == "__main__":
    root = tk.Tk()
    app = WordQuizApp(root)
    root.mainloop()