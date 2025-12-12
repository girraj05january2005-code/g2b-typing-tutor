import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import json, os, time, random

import matplotlib.pyplot as plt
from datetime import datetime

APP_NAME = "G2B Typing Tutor"
APP_VERSION = "1.0.0"

# ---------------- USER DATA SYSTEM ----------------

DATA_DIR = "users"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def load_user_data(username):
    path = os.path.join(DATA_DIR, username + ".json")
    if not os.path.exists(path):
        return {
            "best_wpm": 0,
            "last_wpm": 0,
            "total_tests": 0,
            "lessons_completed": 0,
            "practice_time": 0,
            "history": [],
            "streak": 0,
            "last_practice": ""
        }

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # अगर पुराने data में ये keys नहीं हैं तो add कर दो
        if "history" not in data:
            data["history"] = []
        if "streak" not in data:
            data["streak"] = 0
        if "last_practice" not in data:
            data["last_practice"] = ""

        return data

    except:
        return {
            "best_wpm": 0,
            "last_wpm": 0,
            "total_tests": 0,
            "lessons_completed": 0,
            "practice_time": 0,
            "history": [],
            "streak": 0,
            "last_practice": ""
        }


# ---------------- LESSON DATA ----------------

EN_LESSONS = [
    {
        "title": "EN Lesson 1 - Home Row Left (A S D F)",
        "instruction": "Place your left-hand fingers on A, S, D, F and type the text below.",
        "text": "asdf asdf asdf asdf\nasdf asdf asdf asdf"
    },
    {
        "title": "EN Lesson 2 - Home Row Right (J K L ;)",
        "instruction": "Place your right-hand fingers on J, K, L, ; and type the text below.",
        "text": "jkl; jkl; jkl; jkl;\njkl; jkl; jkl; jkl;"
    },
    {
        "title": "EN Lesson 3 - Simple Words",
        "instruction": "Use both hands to type these simple words.",
        "text": "sad dad lad fall\nask salad flask\nsad lad ask"
    },
    {
        "title": "EN Lesson 4 - Simple Sentence",
        "instruction": "Type this simple sentence without looking at the keyboard.",
        "text": "This is a basic typing lesson.\nPractice slowly and stay relaxed."
    },
    {
        "title": "EN Lesson 5 - Numbers Row",
        "instruction": "Practice typing numbers without looking at the keys.",
        "text": "12345 67890 10203 40506 70809 98765 43210"
    },
    {
        "title": "EN Lesson 6 - Symbols",
        "instruction": "Practice common symbols used while coding or writing.",
        "text": "! @ # $ % ^ & * () [] {} <> ? / \\ |"
    },
    {
        "title": "EN Lesson 7 - Capital Letters",
        "instruction": "Use the Shift key to type capital letters.",
        "text": "A S D F G H J K L Q W E R T Y U I O P"
    },
    {
        "title": "EN Lesson 8 - Word Drills",
        "instruction": "Practice common English words to increase typing speed.",
        "text": "time love work power speed typing master keyboard practice focus learn grow"
    },
    {
        "title": "EN Lesson 9 - Long Paragraph",
        "instruction": "Type the paragraph without looking at your keyboard.",
        "text": "Typing is a very important skill in today's digital world. The more you practice, the faster and more accurate you become. Practice daily to improve your typing speed and accuracy."
    }
]

HI_LESSONS = [
    {
        "title": "HI Lesson 1 - अक्षर (क ख ग घ)",
        "instruction": "हिंदी के अक्षर क ख ग घ की practice करें।",
        "text": "क ख ग घ\nकक खख गग घघ\nक ख ग घ क ख ग घ"
    },
    {
        "title": "HI Lesson 2 - हिंदी वाक्य",
        "instruction": "नीचे दिया गया हिंदी वाक्य टाइप करें।",
        "text": "कभी हार मत मानो क्योंकि बड़ी चीज़ें समय लेती हैं।\nधीरे-धीरे सही, लेकिन रुकना मत।"
    },
    {
        "title": "HI Lesson 3 - सामान्य हिंदी शब्द",
        "instruction": "इन आम हिंदी शब्दों को टाइप करने की practice करें।",
        "text": "किताब परिवार विद्यालय भारत भाषा समय मेहनत अभ्यास ऊर्जा सफलता प्रेरणा"
    },
    {
        "title": "HI Lesson 4 - संपूर्ण वाक्य",
        "instruction": "नीचे दिया गया वाक्य बिना keyboard देखे टाइप करें।",
        "text": "सही तरीके से टाइपिंग सीखने के लिए नियमित अभ्यास करना बहुत आवश्यक होता है।"
    },
    {
        "title": "HI Lesson 5 - लंबा अनुच्छेद",
        "instruction": "इस अनुच्छेद को धीरे धीरे और सही ढंग से टाइप करें।",
        "text": "हिंदी टाइपिंग सीखना शुरू में थोड़ा कठिन लगता है, लेकिन थोड़ी सी मेहनत और रोज़ाना अभ्यास से यह बहुत आसान हो जाता है। धैर्य और निरंतर प्रयास से आप बहुत अच्छी टाइपिंग गति हासिल कर सकते हैं।"
    }
]


TEST_PASSAGES_EN = [
    "The quick brown fox jumps over the lazy dog. Practice daily for better speed.",
    "Typing improves with consistent practice. Keep your eyes on the screen.",
    "Accuracy is more important than speed. Type slowly and correctly first."
]

TEST_PASSAGES_HI = [
    "कभी हार मत मानो क्योंकि बड़ी चीज़ें समय लेती हैं। धीरे-धीरे सही, लेकिन रुकना मत।",
    "मेहनत करने वालों की कभी हार नहीं होती, बस practice जारी रखो।"
]


# ---------------- ON-SCREEN KEYBOARD ----------------

class KeyboardView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.keys = {}
        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

        for row in rows:
            f = tk.Frame(self)
            f.pack()
            for ch in row:
                lbl = tk.Label(f, text=ch, width=3, relief="solid", font=("Arial", 11))
                lbl.pack(side="left", padx=2, pady=2)
                self.keys[ch] = lbl

        self.default_bg = list(self.keys.values())[0].cget("bg")

    def highlight(self, ch):
        ch = ch.upper()
        for lbl in self.keys.values():
            lbl.config(bg=self.default_bg)
        if ch in self.keys:
            self.keys[ch].config(bg="#90EE90")


# ---------------- MAIN APPLICATION CLASS ----------------

class TypingTutorApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x680")

        # Login
        self.root.withdraw()
        username = simpledialog.askstring("User Login", "Enter your user name:")
        if not username:
            username = "Guest"
        self.username = username
        self.data = load_user_data(self.username)

        self.root.title(f"{APP_NAME} v{APP_VERSION} - {self.username}")

        self.root.deiconify()

        # Top bar
        top = tk.Frame(self.root)
        top.pack(fill="x", pady=5)

        # Status label (user + stats + streak)
        self.status_label = tk.Label(top, font=("Arial", 11, "bold"))
        self.status_label.pack(side="left", padx=10)
        self.update_status()

        tk.Button(top, text="Lesson Mode", command=self.show_lesson_mode).pack(side="right", padx=5)
        tk.Button(top, text="Test Mode", command=self.show_test_mode).pack(side="right", padx=5)
        tk.Button(top, text="Report", command=self.show_report).pack(side="right", padx=5)

        self.content = tk.Frame(self.root)
        self.content.pack(fill="both", expand=True, padx=10, pady=10)

        # State
        self.language = "EN"
        self.lesson_index = 0
        self.lesson_target = ""

        self.test_language = "EN"
        self.test_running = False
        self.test_duration = 60
        self.test_remaining = 0
        self.test_start = 0
        self.test_passage = random.choice(TEST_PASSAGES_EN)

        self.show_lesson_mode()
    def update_status(self):
        d = self.data
        text = (
            f"User: {self.username} | "
            f"Best WPM: {d.get('best_wpm', 0):.1f} | "
            f"Last WPM: {d.get('last_wpm', 0):.1f} | "
            f"Lessons: {d.get('lessons_completed', 0)} | "
            f"Tests Taken: {d.get('total_tests', 0)} | "
            f"Streak: {d.get('streak', 0)} days"
        )
        self.status_label.config(text=text)
    # ---------------- Utility ----------------

    def clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ---------------- REPORT WINDOW ----------------
    def show_report(self):
        report = tk.Toplevel(self.root)
        report.title("User Report")
        report.geometry("420x380")

        d = self.data

        text = (
            f"{APP_NAME} v{APP_VERSION}\n"
            f"User: {self.username}\n"
            f"---------------------------\n"
            f"Best WPM: {d.get('best_wpm', 0):.1f}\n"
            f"Last WPM: {d.get('last_wpm', 0):.1f}\n"
            f"Total Tests: {d.get('total_tests', 0)}\n"
            f"Lessons Completed: {d.get('lessons_completed', 0)}\n"
            f"Practice Time: {d.get('practice_time', 0)} sec\n"
            f"Daily Streak: {d.get('streak', 0)} days\n"
            f"Last Practice: {d.get('last_practice', 'N/A')}\n"
        )

        tk.Label(report, text=text, justify="left", font=("Arial", 12)).pack(pady=10)

        btn_frame = tk.Frame(report)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Show WPM Graph",
                  command=self.show_wpm_graph).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Close",
                  command=report.destroy).grid(row=0, column=1, padx=5)
    def show_wpm_graph(self):
        history = self.data.get("history", [])
        if not history:
            # Hindi: कोई test history नहीं है। पहले कुछ tests चलाएँ।
            messagebox.showinfo("No Data", "No test history found. Please run some tests first.")
            return

        wpms = [h["wpm"] for h in history]
        tests = list(range(1, len(history) + 1))

        plt.figure(figsize=(6, 4))
        plt.plot(tests, wpms, marker="o")
        plt.title(f"{self.username} - WPM History")
        plt.xlabel("Test Number")
        plt.ylabel("WPM")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # ---------------- LESSON MODE ----------------

    def show_lesson_mode(self):
        self.clear()

        tk.Label(self.content, text="Lesson Mode", font=("Arial", 16, "bold")).pack(pady=5)

        lang_frame = tk.Frame(self.content)
        lang_frame.pack()

        tk.Button(lang_frame, text="English", command=lambda: self.set_language("EN")).grid(row=0, column=0, padx=5)
        tk.Button(lang_frame, text="Hindi", command=lambda: self.set_language("HI")).grid(row=0, column=1, padx=5)

        self.lesson_title = tk.Label(self.content, text="", font=("Arial", 14, "bold"))
        self.lesson_title.pack(pady=4)

        self.lesson_instruction = tk.Label(self.content, text="", wraplength=850, justify="left")
        self.lesson_instruction.pack(pady=3)

        self.lesson_text_box = tk.Text(self.content, height=5, width=100, font=("Consolas", 13))
        self.lesson_text_box.pack(pady=4)
        self.lesson_text_box.config(state="disabled", bg="#e9e9e9")

        tk.Label(self.content, text="Type here:", font=("Arial", 11, "bold")).pack(anchor="w")

        self.lesson_input = tk.Text(self.content, height=6, width=100, font=("Consolas", 13))
        self.lesson_input.pack(pady=4)
        self.lesson_input.bind("<KeyRelease>", self.lesson_typing)

        self.lesson_accuracy = tk.Label(self.content, text="Accuracy: 0%", font=("Arial", 12))
        self.lesson_accuracy.pack(pady=4)

        tk.Label(self.content, text="On-screen Keyboard (English)", font=("Arial", 10)).pack()
        self.keyboard = KeyboardView(self.content)
        self.keyboard.pack(pady=3)

        nav = tk.Frame(self.content)
        nav.pack()

        tk.Button(nav, text="Previous", command=self.prev_lesson).grid(row=0, column=0, padx=5)
        tk.Button(nav, text="Next", command=self.next_lesson).grid(row=0, column=1, padx=5)
        tk.Button(nav, text="Restart", command=self.restart_lesson).grid(row=0, column=2, padx=5)

        self.set_language(self.language)

    def set_language(self, lang):
        self.language = lang
        self.lesson_index = 0
        self.load_lesson()

    def get_lessons(self):
        return EN_LESSONS if self.language == "EN" else HI_LESSONS

    def load_lesson(self):
        lessons = self.get_lessons()
        data = lessons[self.lesson_index]

        self.lesson_title.config(text=data["title"])
        self.lesson_instruction.config(text=data["instruction"])
        self.lesson_target = data["text"]

        self.lesson_text_box.config(state="normal")
        self.lesson_text_box.delete("1.0", "end")
        self.lesson_text_box.insert("1.0", data["text"])
        self.lesson_text_box.config(state="disabled")

        self.lesson_input.delete("1.0", "end")
        self.lesson_accuracy.config(text="Accuracy: 0%")

    def lesson_typing(self, event=None):
        typed = self.lesson_input.get("1.0", "end-1c")
        target = self.lesson_target

        correct = 0
        for i in range(min(len(typed), len(target))):
            if typed[i] == target[i]:
                correct += 1

        acc = (correct / len(typed) * 100) if typed else 0
        self.lesson_accuracy.config(text=f"Accuracy: {acc:.1f}%")

        if self.language == "EN" and typed:
            last = typed[-1]
            if last.isalpha():
                self.keyboard.highlight(last)

        if acc == 100 and len(typed) >= len(target):
            self.data["lessons_completed"] += 1
            save_user_data(self.username, self.data)

    def prev_lesson(self):
        if self.lesson_index > 0:
            self.lesson_index -= 1
            self.load_lesson()

    def next_lesson(self):
        lessons = self.get_lessons()
        if self.lesson_index < len(lessons) - 1:
            self.lesson_index += 1
            self.load_lesson()
        else:
            messagebox.showinfo("Done", "No more lessons here!")

    def restart_lesson(self):
        self.load_lesson()

    # ---------------- TEST MODE ----------------

    def show_test_mode(self):
        self.clear()

        tk.Label(self.content, text="Typing Test", font=("Arial", 16, "bold")).pack(pady=5)

        # language buttons
        lang_frame = tk.Frame(self.content)
        lang_frame.pack()
        tk.Button(lang_frame, text="English", command=lambda: self.set_test_language("EN")).grid(row=0, column=0, padx=5)
        tk.Button(lang_frame, text="Hindi", command=lambda: self.set_test_language("HI")).grid(row=0, column=1, padx=5)

        # passage label
        self.test_passage_label = tk.Label(
            self.content,
            text=self.test_passage,
            wraplength=850,
            justify="left",
            font=("Arial", 12)
        )
        self.test_passage_label.pack(pady=10)

        tk.Label(self.content, text="Type here:", font=("Arial", 11, "bold")).pack(anchor="w")

        # typing box
        self.test_input = tk.Text(self.content, height=6, width=100, font=("Consolas", 13))
        self.test_input.pack(pady=4)
        self.test_input.config(state="disabled")

        # control buttons
        control = tk.Frame(self.content)
        control.pack(pady=5)

        self.start_btn = tk.Button(control, text="Start Test", command=self.start_test)
        self.start_btn.grid(row=0, column=0, padx=5)

        tk.Button(control, text="New Passage", command=self.new_passage).grid(row=0, column=1, padx=5)

        # timer label
        self.timer_label = tk.Label(self.content, text=f"Time: {self.test_duration}", font=("Arial", 13, "bold"))
        self.timer_label.pack(pady=4)

        # progress bar
        self.progress = ttk.Progressbar(self.content, orient="horizontal", length=600, mode="determinate")
        self.progress.pack(pady=2)
        self.progress["maximum"] = self.test_duration
        self.progress["value"] = 0

        # results labels
        self.wpm_label = tk.Label(self.content, text="WPM: 0", font=("Arial", 12))
        self.wpm_label.pack(pady=2)

        self.acc_label = tk.Label(self.content, text="Accuracy: 0%", font=("Arial", 12))
        self.acc_label.pack(pady=2)

    def set_test_language(self, lang):
        self.test_language = lang
        self.new_passage()

    def new_passage(self):
        if self.test_language == "EN":
            self.test_passage = random.choice(TEST_PASSAGES_EN)
        else:
            self.test_passage = random.choice(TEST_PASSAGES_HI)

        self.test_passage_label.config(text=self.test_passage)

    def start_test(self):
        self.test_running = True
        self.start_time = time.time()
        self.test_remaining = self.test_duration

        # reset UI
        self.timer_label.config(text=f"Time: {self.test_duration}")
        self.progress["value"] = 0

        self.test_input.config(state="normal")
        self.test_input.delete("1.0", "end")
        self.test_input.focus_set()

        self.start_btn.config(state="disabled")

        # start timer loop
        self.update_test_timer()

    def update_test_timer(self):
        if not self.test_running:
            return

        elapsed = time.time() - self.start_time
        remaining = int(self.test_duration - elapsed)

        if remaining < 0:
            remaining = 0

        # update UI
        self.progress["value"] = elapsed
        self.timer_label.config(text=f"Time: {remaining}")

        if remaining <= 0:
            self.finish_test()
            return

        self.root.after(100, self.update_test_timer)

    def finish_test(self):
        self.test_running = False
        self.start_btn.config(state="normal")
        self.test_input.config(state="disabled")

        typed = self.test_input.get("1.0", "end-1c")
        chars = len(typed)

        if chars == 0:
            messagebox.showinfo("Result", "You did not type anything.")
            return

        elapsed = max(time.time() - self.start_time, 1)
        minutes = elapsed / 60

        wpm = (chars / 5) / minutes

        correct = 0
        for i in range(min(len(typed), len(self.test_passage))):
            if typed[i] == self.test_passage[i]:
                correct += 1

        accuracy = (correct / chars * 100) if chars else 0

        self.wpm_label.config(text=f"WPM: {wpm:.1f}")
        self.acc_label.config(text=f"Accuracy: {accuracy:.1f}%")

        # update history
        if "history" not in self.data:
            self.data["history"] = []

        self.data["history"].append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "wpm": round(wpm, 1),
            "accuracy": round(accuracy, 1),
            "language": self.test_language,
            "duration": self.test_duration
        })

        # update summary fields
        self.data["last_wpm"] = round(wpm, 1)
        self.data["best_wpm"] = max(self.data["best_wpm"], wpm)
        self.data["total_tests"] += 1
        self.data["practice_time"] += int(elapsed)

        # daily streak system
        today = datetime.now().strftime("%Y-%m-%d")
        last = self.data.get("last_practice", "")

        from datetime import timedelta
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        if last == today:
            # already counted today
            pass
        elif last == yesterday:
            # previous day was also practice → streak+1
            self.data["streak"] += 1
        else:
            # gap → reset streak
            self.data["streak"] = 1

        self.data["last_practice"] = today

        save_user_data(self.username, self.data)

        messagebox.showinfo("Result", f"WPM: {wpm:.1f}\nAccuracy: {accuracy:.1f}%")
        self.update_status()
# ---------------- RUN APP ----------------

if __name__ == "__main__":
    root = tk.Tk()
    TypingTutorApp(root)
    root.mainloop()
