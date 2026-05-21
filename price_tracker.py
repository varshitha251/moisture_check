import tkinter as tk
from tkinter import messagebox
import random
import datetime
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGIN_FILE = os.path.join(SCRIPT_DIR, "login.txt")
DATA_FILE = os.path.join(SCRIPT_DIR, "irrigation_data.txt")

# ============== GLASSMORPHISM THEME ==============
BG_COLOR = "#0f1419"          # Deep dark background
GLASS_LIGHT = "#1e2329"       # Light glass card
GLASS_DARK = "#161a1f"        # Darker glass
ACCENT_PRIMARY = "#4ecca3"    # Fresh teal green
ACCENT_SECONDARY = "#39b894"  # Darker teal
BUTTON_PRIMARY = "#4ecca3"
BUTTON_HOVER = "#39b894"
BUTTON_DANGER = "#ff6b6b"
BUTTON_WARNING = "#ffa500"
TEXT_PRIMARY = "#e0e0e0"
TEXT_SECONDARY = "#a0a0a0"
BORDER_COLOR = "#2e3339"

# ================= LOGIN FUNCTION =================
def check_login():
    global username_entry, password_entry
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    try:
        with open(LOGIN_FILE, "r") as file:
            for line in file:
                if not line.strip():
                    continue
                u, p = line.strip().split(",")
                if username == u and password == p:
                    login_window.destroy()
                    open_dashboard(username)
                    return

        messagebox.showerror("Login Failed", "Invalid username or password.")

    except FileNotFoundError:
        messagebox.showerror("File Not Found", "login.txt file not found.")


# ================= DASHBOARD =================
def open_dashboard(user):
    root = tk.Tk()
    root.title("Smart Irrigation System")
    root.geometry("700x850")
    root.configure(bg=BG_COLOR)
    root.resizable(False, False)

    threshold_value = tk.IntVar(value=40)
    auto_running = tk.BooleanVar(value=False)
    last_check_text = tk.StringVar(value="Last update: --")

    def create_glass_card(parent, **kwargs):
        """Create a glassmorphism card with rounded effect"""
        card = tk.Frame(parent, bg=GLASS_LIGHT, relief="flat", bd=0, **kwargs)
        return card

    def save_history(moisture, tank, pump_status):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(DATA_FILE, "a") as file:
            file.write(
                f"{current_time} | User:{user} | Moisture:{moisture}% | Tank:{tank}% | Pump:{pump_status}\n"
            )
        last_check_text.set(f"Last update: {current_time}")

    def update_status(moisture, tank_level, pump_status, pump_color, pump_text):
        moisture_value_label.config(text=f"{moisture}%")
        tank_value_label.config(text=f"{tank_level}%")
        pump_status_label.config(text=pump_text, fg=pump_color)

    def check_moisture():
        moisture = random.randint(0, 100)
        tank_level = random.randint(10, 100)
        threshold = threshold_value.get()

        if tank_level <= 20:
            pump_status = "OFF (Low Tank)"
            color = BUTTON_WARNING
            label = "⚠ Pump OFF — Fill tank"
        elif moisture < threshold:
            pump_status = "ON"
            color = ACCENT_PRIMARY
            label = "✓ Pump ON — Irrigating"
        else:
            pump_status = "OFF"
            color = "#888888"
            label = "◉ Pump OFF — Soil moist"

        update_status(moisture, tank_level, pump_status, color, label)
        save_history(moisture, tank_level, pump_status)

    def toggle_auto_mode():
        if auto_running.get():
            auto_running.set(False)
            auto_button.config(text="► Start Auto Mode")
            status_footer_label.config(text="Auto mode stopped.")
        else:
            auto_running.set(True)
            auto_button.config(text="⏸ Stop Auto Mode")
            status_footer_label.config(text="Auto mode running — checking every 5 seconds")
            root.after(5000, auto_cycle)

    def auto_cycle():
        if auto_running.get():
            check_moisture()
            root.after(5000, auto_cycle)

    def view_history():
        history_window = tk.Toplevel(root)
        history_window.title("Irrigation History")
        history_window.geometry("700x500")
        history_window.configure(bg=BG_COLOR)
        history_window.resizable(False, False)

        history_title = tk.Label(
            history_window,
            text="📋 Irrigation History Log",
            font=("Segoe UI", 18, "bold"),
            bg=BG_COLOR,
            fg=ACCENT_PRIMARY,
        )
        history_title.pack(pady=16)

        history_frame = create_glass_card(history_window, padx=16, pady=16)
        history_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        text_area = tk.Text(
            history_frame,
            wrap="word",
            bg=GLASS_DARK,
            fg=TEXT_PRIMARY,
            font=("Consolas", 10),
            insertbackground=ACCENT_PRIMARY,
            selectbackground=ACCENT_PRIMARY,
            selectforeground=BG_COLOR,
        )
        text_area.pack(fill="both", expand=True, padx=0, pady=0)
        text_area.configure(state="disabled")

        try:
            with open(DATA_FILE, "r") as file:
                data = file.read().strip()
                text_area.configure(state="normal")
                text_area.delete("1.0", tk.END)
                text_area.insert("1.0", data if data else "No data available yet.")
                text_area.configure(state="disabled")
        except FileNotFoundError:
            text_area.configure(state="normal")
            text_area.insert("1.0", "No data available yet.")
            text_area.configure(state="disabled")

    def logout():
        root.destroy()
        main()

    # ========== HEADER ==========
    header_frame = create_glass_card(root, padx=24, pady=20)
    header_frame.pack(fill="x", padx=16, pady=(16, 8))

    title_label = tk.Label(
        header_frame,
        text="🌾 Smart Irrigation System",
        font=("Segoe UI", 24, "bold"),
        bg=GLASS_LIGHT,
        fg=ACCENT_PRIMARY,
    )
    title_label.pack(anchor="w")

    welcome_label = tk.Label(
        header_frame,
        text=f"Welcome back, {user}",
        font=("Segoe UI", 11),
        bg=GLASS_LIGHT,
        fg=TEXT_SECONDARY,
    )
    welcome_label.pack(anchor="w", pady=(6, 0))

    # ========== STATS CARDS ==========
    stats_frame = tk.Frame(root, bg=BG_COLOR)
    stats_frame.pack(fill="x", padx=16, pady=8)

    def create_stat_card(parent, title, emoji):
        card = create_glass_card(parent, padx=16, pady=18)
        card.pack(side="left", fill="both", expand=True, padx=6)

        title_label = tk.Label(
            card,
            text=f"{emoji} {title}",
            font=("Segoe UI", 11, "bold"),
            bg=GLASS_LIGHT,
            fg=TEXT_SECONDARY,
        )
        title_label.pack(anchor="w", pady=(0, 8))

        value_label = tk.Label(
            card,
            text="--%",
            font=("Segoe UI", 28, "bold"),
            bg=GLASS_LIGHT,
            fg=ACCENT_PRIMARY,
        )
        value_label.pack(anchor="w")

        return value_label

    moisture_value_label = create_stat_card(stats_frame, "Soil Moisture", "💧")
    tank_value_label = create_stat_card(stats_frame, "Tank Level", "🏊")
    pump_status_label = tk.Label(
        create_glass_card(stats_frame, padx=16, pady=18),
        text="--",
        font=("Segoe UI", 13, "bold"),
        bg=GLASS_LIGHT,
        fg=TEXT_PRIMARY,
        wraplength=150,
        justify="left",
    )
    pump_status_label.pack(side="left", fill="both", expand=True, padx=6)

    # ========== THRESHOLD CONTROL ==========
    threshold_frame = create_glass_card(root, padx=20, pady=20)
    threshold_frame.pack(fill="x", padx=16, pady=8)

    tk.Label(
        threshold_frame,
        text="⚙️  Moisture Threshold",
        font=("Segoe UI", 13, "bold"),
        bg=GLASS_LIGHT,
        fg=ACCENT_PRIMARY,
    ).pack(anchor="w", pady=(0, 4))

    tk.Label(
        threshold_frame,
        text="Set the soil moisture level to trigger irrigation",
        font=("Segoe UI", 10),
        bg=GLASS_LIGHT,
        fg=TEXT_SECONDARY,
    ).pack(anchor="w", pady=(0, 12))

    threshold_scale = tk.Scale(
        threshold_frame,
        from_=10,
        to=90,
        orient="horizontal",
        variable=threshold_value,
        length=550,
        bg=GLASS_LIGHT,
        fg=ACCENT_PRIMARY,
        troughcolor=GLASS_DARK,
        highlightthickness=0,
        activebackground=BUTTON_HOVER,
    )
    threshold_scale.pack(fill="x")

    # ========== CONTROL BUTTONS ==========
    button_container = create_glass_card(root, padx=0, pady=0)
    button_container.pack(fill="x", padx=16, pady=8)

    def create_button(parent, text, command, bg, fg=TEXT_PRIMARY, width=None):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=BUTTON_HOVER if bg == BUTTON_PRIMARY else bg,
            activeforeground=fg,
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=12,
            pady=12,
            cursor="hand2",
            relief="flat",
        )
        return btn

    btn_check = create_button(button_container, "📊 Check Moisture", check_moisture, BUTTON_PRIMARY)
    btn_check.pack(side="left", fill="both", expand=True, padx=4, pady=8)

    btn_history = create_button(button_container, "📋 History", view_history, BUTTON_PRIMARY)
    btn_history.pack(side="left", fill="both", expand=True, padx=4, pady=8)

    btn_logout = create_button(button_container, "🚪 Logout", logout, GLASS_DARK)
    btn_logout.pack(side="left", fill="both", expand=True, padx=4, pady=8)

    # ========== AUTO MODE & EXIT ==========
    mode_frame = create_glass_card(root, padx=0, pady=0)
    mode_frame.pack(fill="x", padx=16, pady=8)

    auto_button = create_button(mode_frame, "► Start Auto Mode", toggle_auto_mode, BUTTON_WARNING)
    auto_button.pack(side="left", fill="both", expand=True, padx=4, pady=8)

    exit_button = create_button(mode_frame, "⨉ Exit", root.destroy, BUTTON_DANGER)
    exit_button.pack(side="left", fill="both", expand=True, padx=4, pady=8)

    # ========== FOOTER ==========
    footer_frame = create_glass_card(root, padx=20, pady=16)
    footer_frame.pack(fill="x", padx=16, pady=(8, 16))

    last_check_label = tk.Label(
        footer_frame,
        textvariable=last_check_text,
        font=("Segoe UI", 10),
        bg=GLASS_LIGHT,
        fg=TEXT_SECONDARY,
    )
    last_check_label.pack(anchor="w", pady=(0, 4))

    status_footer_label = tk.Label(
        footer_frame,
        text="Use manual check or auto mode for continuous monitoring",
        font=("Segoe UI", 9),
        bg=GLASS_LIGHT,
        fg=TEXT_SECONDARY,
    )
    status_footer_label.pack(anchor="w")

    root.mainloop()


# ================= MAIN LOGIN WINDOW =================
def main():
    global login_window, username_entry, password_entry

    login_window = tk.Tk()
    login_window.title("Smart Irrigation - Login")
    login_window.geometry("420x480")
    login_window.configure(bg=BG_COLOR)
    login_window.resizable(False, False)

    # Center logo area
    logo_frame = tk.Frame(login_window, bg=BG_COLOR)
    logo_frame.pack(pady=(32, 24))

    logo_label = tk.Label(
        logo_frame,
        text="🌾",
        font=("Segoe UI", 64),
        bg=BG_COLOR,
    )
    logo_label.pack()

    # Login form card
    login_frame = tk.Frame(login_window, bg=GLASS_LIGHT, relief="flat", bd=0, padx=24, pady=28)
    login_frame.pack(expand=True, fill="both", padx=20, pady=(0, 32))

    tk.Label(
        login_frame,
        text="Smart Irrigation System",
        font=("Segoe UI", 18, "bold"),
        bg=GLASS_LIGHT,
        fg=ACCENT_PRIMARY,
    ).pack(pady=(0, 6))

    tk.Label(
        login_frame,
        text="Enter your credentials to continue",
        font=("Segoe UI", 10),
        bg=GLASS_LIGHT,
        fg=TEXT_SECONDARY,
    ).pack(pady=(0, 24))

    # Username field
    tk.Label(
        login_frame,
        text="👤 Username",
        font=("Segoe UI", 10, "bold"),
        bg=GLASS_LIGHT,
        fg=TEXT_PRIMARY,
    ).pack(anchor="w", pady=(0, 6))

    username_entry = tk.Entry(
        login_frame,
        font=("Segoe UI", 11),
        bd=1,
        relief="solid",
        bg=GLASS_DARK,
        fg=TEXT_PRIMARY,
        insertbackground=ACCENT_PRIMARY,
        width=25,
        takefocus=True,
        state="normal",
    )
    username_entry.pack(fill="x", pady=(0, 14))
    login_frame.after(100, username_entry.focus_set)

    # Password field
    tk.Label(
        login_frame,
        text="🔐 Password",
        font=("Segoe UI", 10, "bold"),
        bg=GLASS_LIGHT,
        fg=TEXT_PRIMARY,
    ).pack(anchor="w", pady=(0, 6))

    password_entry = tk.Entry(
        login_frame,
        show="•",
        font=("Segoe UI", 11),
        bd=1,
        relief="solid",
        bg=GLASS_DARK,
        fg=TEXT_PRIMARY,
        insertbackground=ACCENT_PRIMARY,
        width=25,
        takefocus=True,
        state="normal",
    )
    password_entry.pack(fill="x", pady=(0, 20))

    # Login button
    login_button = tk.Button(
        login_frame,
        text="🔓 Login",
        command=check_login,
        bg=BUTTON_PRIMARY,
        fg=BG_COLOR,
        activebackground=BUTTON_HOVER,
        activeforeground=BG_COLOR,
        font=("Segoe UI", 12, "bold"),
        bd=0,
        pady=11,
        cursor="hand2",
        relief="flat",
    )
    login_button.pack(fill="x")

    # Bind Enter key to login
    login_window.bind("<Return>", lambda event: check_login())

    login_window.mainloop()


# ================= ENTRY POINT =================
if __name__ == "__main__":
    main()