import tkinter as tk
from datetime import datetime

# IMPORT YOUR EXISTING LOGICS
from chatbot import chatbot_response

# ================== THEMES ==================
THEMES = {
    "dark": {
        "BG": "#0f7c7e",
        "HEADER": "#0b5f61",
        "SIDEBAR": "#094b4d",
        "USER": "#cfeeee",
        "BOT": "#ffffff",
        "TEXT": "#e9ffff",
        "DOMAIN_TEXT": "#e6ffff",
        "BTN": "#ffffff",
        "BTN_TEXT": "#0b5f61",
        "TIME": "#e0f5f5"
    },
    "light": {
        "BG": "#eef7f7",
        "HEADER": "#d9eeee",
        "SIDEBAR": "#cfe6e6",
        "USER": "#dcf3f3",
        "BOT": "#ffffff",
        "TEXT": "#0b5f61",
        "DOMAIN_TEXT": "#0b5f61",
        "BTN": "#0f7c7e",
        "BTN_TEXT": "#ffffff",
        "TIME": "#555555"
    }
}

current_theme = "dark"

def theme(key):
    return THEMES[current_theme][key]

# ================== WINDOW ==================
root = tk.Tk()
root.title("SCRAPBOT – Intelligent Assistant")
root.geometry("1100x650")
root.minsize(900, 550)

# ================== HEADER ==================
header = tk.Label(
    root,
    text="SCRAPBOT-Intelligent",
    font=("Segoe UI", 18, "bold"),
    pady=12
)
header.pack(fill="x")

# ================== MAIN ==================
main = tk.Frame(root)
main.pack(fill="both", expand=True)

# ================== SIDEBAR ==================
sidebar = tk.Frame(main, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

domain_label = tk.Label(
    sidebar,
    text="Domains",
    font=("Segoe UI", 14, "bold"),
    pady=12
)
domain_label.pack(fill="x")

domains = [
    "🍔 Food",
    "✈️ Flights",
    "🧳 Trips",
    "🛒 E‑Commerce",
    "🚗 Automobiles",
    "💼 Jobs"
]

domain_widgets = []

def select_domain(domain_name):
    add_message(f"🔹 Domain switched to {domain_name}", "bot")

def on_enter(e):
    e.widget.config(bg=theme("BTN"), fg=theme("BTN_TEXT"))

def on_leave(e):
    e.widget.config(bg=theme("SIDEBAR"), fg=theme("DOMAIN_TEXT"))

for d in domains:
    lbl = tk.Label(
        sidebar,
        text=d,
        anchor="w",
        padx=20,
        pady=10,
        font=("Segoe UI", 11)
    )
    lbl.pack(fill="x")
    lbl.bind("<Button-1>", lambda e, n=d: select_domain(n))
    lbl.bind("<Enter>", on_enter)
    lbl.bind("<Leave>", on_leave)
    domain_widgets.append(lbl)

# ================== THEME SWITCH ==================
def toggle_theme():
    global current_theme
    current_theme = "light" if current_theme == "dark" else "dark"
    apply_theme()

theme_btn = tk.Button(
    sidebar,
    text="🌗 Switch Theme",
    font=("Segoe UI", 10, "bold"),
    command=toggle_theme
)
theme_btn.pack(pady=20)

# ================== CHAT AREA ==================
chat_area = tk.Frame(main)
chat_area.pack(side="right", fill="both", expand=True)

canvas = tk.Canvas(chat_area, highlightthickness=0)
scrollbar = tk.Scrollbar(chat_area, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

chat_frame = tk.Frame(canvas)
canvas_window = canvas.create_window((0, 0), window=chat_frame, anchor="nw")

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def update_scroll(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(1)

chat_frame.bind("<Configure>", update_scroll)

def resize_canvas(event):
    canvas.itemconfig(canvas_window, width=event.width)

canvas.bind("<Configure>", resize_canvas)

# ================== MESSAGE ==================
def add_message(text, sender):
    max_width = int(canvas.winfo_width() * 0.65)

    row = tk.Frame(chat_frame, bg=theme("BG"))
    row.pack(fill="x", pady=6, padx=14)

    bubble_bg = theme("USER") if sender == "user" else theme("BOT")
    anchor = "e" if sender == "user" else "w"

    bubble = tk.Label(
        row,
        text=text,
        bg=bubble_bg,
        fg="#000000",
        font=("Segoe UI", 10),
        wraplength=max_width,
        justify="left",
        padx=14,
        pady=10
    )
    bubble.pack(anchor=anchor)

    time = tk.Label(
        row,
        text=datetime.now().strftime("%H:%M"),
        font=("Segoe UI", 8),
        bg=theme("BG"),
        fg=theme("TIME")
    )
    time.pack(anchor=anchor, padx=6)

    update_scroll()
    return bubble

# ================== TYPING EFFECT ==================
def typing(text, i=0, bubble=None):
    if i == 0:
        bubble = add_message("…", "bot")

    bubble.config(text=text[:i])

    if i < len(text):
        root.after(12, typing, text, i + 1, bubble)

# ================== SEND ==================
def send():
    msg = entry.get().strip()
    if not msg:
        return

    add_message(msg, "user")
    entry.delete(0, tk.END)

    reply = chatbot_response(msg)
    typing(reply)

# ================== INPUT ==================
input_bar = tk.Frame(root)
input_bar.pack(fill="x", pady=8)

entry = tk.Entry(input_bar, font=("Segoe UI", 11), bd=0)
entry.pack(side="left", fill="x", expand=True, padx=12, pady=10)
entry.bind("<Return>", lambda e: send())

send_btn = tk.Button(
    input_bar,
    text="Send",
    font=("Segoe UI", 10, "bold"),
    command=send
)
send_btn.pack(side="right", padx=12)

# ================== APPLY THEME ==================
def apply_theme():
    root.configure(bg=theme("BG"))
    header.configure(bg=theme("HEADER"), fg=theme("TEXT"))
    main.configure(bg=theme("BG"))
    sidebar.configure(bg=theme("SIDEBAR"))
    chat_area.configure(bg=theme("BG"))
    canvas.configure(bg=theme("BG"))
    chat_frame.configure(bg=theme("BG"))
    input_bar.configure(bg=theme("HEADER"))

    domain_label.configure(bg=theme("SIDEBAR"), fg=theme("DOMAIN_TEXT"))
    theme_btn.configure(bg=theme("BTN"), fg=theme("BTN_TEXT"))

    for w in domain_widgets:
        w.configure(bg=theme("SIDEBAR"), fg=theme("DOMAIN_TEXT"))

apply_theme()

add_message("Hello! How can I help you today?", "bot")

root.mainloop()
