import customtkinter as ctk
import speech_recognition as sr
from textblob import TextBlob
import threading
import random

# App Config
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("🎙️ FeelSense - Your Mood Mirror")
app.geometry("850x550")

# --- TITLE SECTION ---
title = ctk.CTkLabel(
    app,
    text="💬 FeelSense",
    font=("Arial Rounded MT Bold", 32),
    text_color="#00f5d4"
)
title.pack(pady=15)

subtitle = ctk.CTkLabel(
    app,
    text="Speak or type your thoughts — let's decode your emotions 💭",
    font=("Arial", 15),
    text_color="white"
)
subtitle.pack(pady=5)

# --- TEXT INPUT BOX ---
text_box = ctk.CTkTextbox(
    app, width=650, height=150,
    corner_radius=15, font=("Arial", 14),
    fg_color="#1e1e1e", border_color="#00f5d4", border_width=2
)
text_box.pack(pady=15)

# --- RESULT DISPLAY ---
result_label = ctk.CTkLabel(app, text="Sentiment: ", font=("Arial Rounded MT Bold", 22))
result_label.pack(pady=25)

motivation_label = ctk.CTkLabel(app, text="", font=("Arial", 16, "italic"), text_color="#ccc")
motivation_label.pack()

# --- SENTIMENT ANALYSIS FUNCTION ---
def analyze_sentiment():
    text = text_box.get("1.0", "end").strip()
    if not text:
        result_label.configure(text="⚠️ Please enter or speak something!", text_color="gray")
        motivation_label.configure(text="")
        return

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        result, color = "Positive 😊", "#00ff88"
        responses = [
            "You sound full of good vibes! Keep that energy up! 💪",
            "That’s the spirit — stay optimistic and keep shining! ☀️",
            "Wow, someone’s feeling great today! 😄"
        ]
    elif polarity < 0:
        result, color = "Negative 😞", "#ff4d4d"
        responses = [
            "Hey, it's okay to have rough days — they don’t define you ❤️",
            "Take a deep breath — you’ve got this. 💫",
            "Every down moment is a setup for a comeback. 🌈"
        ]
    else:
        result, color = "Neutral 😐", "#00b4d8"
        responses = [
            "Hmm, balanced mood today — calm and steady. 🧘‍♂️",
            "Not too high, not too low — perfect control. ⚖️",
            "Neutral vibes — smooth sailing ahead. 🌤️"
        ]

    result_label.configure(
        text=f"Sentiment: {result}\nPolarity Score: {polarity:.2f}",
        text_color=color
    )
    motivation_label.configure(text=random.choice(responses), text_color=color)

# --- VOICE INPUT FUNCTION ---
def record_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    result_label.configure(text="🎙️ Listening...", text_color="yellow")
    app.update_idletasks()

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
        result_label.configure(text="🧠 Processing voice...", text_color="skyblue")
        app.update_idletasks()

        text = recognizer.recognize_google(audio)
        text_box.delete("1.0", "end")
        text_box.insert("1.0", text)
        result_label.configure(text="✅ Voice captured successfully!", text_color="lime")

        # Auto-analyze after voice input
        analyze_sentiment()

    except sr.UnknownValueError:
        result_label.configure(text="❌ Couldn't understand audio. Try again.", text_color="red")
    except sr.RequestError:
        result_label.configure(text="⚠️ Speech service unavailable.", text_color="orange")
    except sr.WaitTimeoutError:
        result_label.configure(text="⏱️ No voice detected. Try again.", text_color="gray")

# --- BUTTONS ---
def clear_text():
    text_box.delete("1.0", "end")
    result_label.configure(text="Sentiment: ", text_color="white")
    motivation_label.configure(text="")

def start_voice_thread():
    thread = threading.Thread(target=record_voice)
    thread.start()

btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.pack(pady=10)

voice_btn = ctk.CTkButton(btn_frame, text="🎤 Speak", command=start_voice_thread, width=160, height=45, fg_color="#0077b6")
voice_btn.grid(row=0, column=0, padx=12)

analyze_btn = ctk.CTkButton(btn_frame, text="🔍 Analyze", command=analyze_sentiment, width=160, height=45, fg_color="#00b894")
analyze_btn.grid(row=0, column=1, padx=12)

clear_btn = ctk.CTkButton(btn_frame, text="🧹 Clear", command=clear_text, width=160, height=45, fg_color="#ff4d4d")
clear_btn.grid(row=0, column=2, padx=12)

# --- FOOTER ---
footer = ctk.CTkLabel(
    app,
    text="💡 Powered by TextBlob | Designed to uplift your mood 💚",
    font=("Arial", 12),
    text_color="gray"
)
footer.pack(side="bottom", pady=10)

app.mainloop()



