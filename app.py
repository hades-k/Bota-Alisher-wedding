import streamlit as st
import pandas as pd
import os
import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Бота & Алишер",
    page_icon="💍",
    layout="centered" # Use centered layout for better focus
)

# --- File for RSVPs ---
RSVP_FILE = "rsvps.csv"

# --- Load Custom CSS ---
def load_css():
    st.markdown("""
    <style>
    /* Base reset for Streamlit app */
    .stApp {
      font-family: 'Georgia', serif;
      color: #f5f0e1;
      background: #000; /* Fallback for browsers that don't support the gradient */
      overflow: hidden;
      min-height: 100vh;
      position: relative;
    }

    /* Background Layer - applied to injected div */
    .background-layer {
      position: fixed;
      inset: 0;
      background: linear-gradient(to bottom, #0a0f1c, #000000);
      z-index: -3; /* Ensure it's behind Streamlit content */
    }

    /* Subtle golden stars - applied to injected div */
    .stars-layer {
      position: fixed; /* Use fixed to cover the whole viewport */
      inset: 0;
      width: 100%;
      height: 100%;
      background-image: radial-gradient(#bfa76f 1px, transparent 1px);
      background-size: 3px 3px;
      opacity: 0.1;
      animation: twinkle 8s infinite ease-in-out;
      z-index: -2; /* Behind content, above background-layer */
    }

    /* Light golden aura - applied to injected div */
    .aura-layer {
      position: fixed; /* Use fixed to cover the whole viewport */
      top: -10%;
      left: -10%;
      width: 120%;
      height: 120%;
      background: radial-gradient(ellipse at center, rgba(191, 167, 111, 0.1), transparent 70%);
      z-index: -2; /* Same as stars, or adjust as needed */
    }

    /* Optional dark overlay for better contrast - applied to injected div */
    .overlay-layer {
      position: fixed; /* Use fixed to cover the whole viewport */
      inset: 0;
      background-color: rgba(0, 0, 0, 0.4);
      z-index: -1; /* Behind content, above other layers */
    }

    /* Streamlit specific adjustments */
    .main .block-container {
        background-color: rgba(0, 0, 0, 0.85); /* Keep existing dark container */
        border: 2px solid #feda4a;
        box-shadow: 0 0 30px 10px #feda4a;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        z-index: 1; /* Ensure Streamlit content is above background layers */
        position: relative; /* Needed for z-index to work */
    }

    /* Typography */
    h1, h2, h3, p, label, .st-emotion-cache-16txtl3 {
        font-family: 'Orbitron', sans-serif; /* Keep existing font */
        color: #feda4a; /* Keep existing color */
        text-shadow: 0 0 5px #000, 0 0 10px #000;
    }
    h1 { text-transform: uppercase; }
    h2 { color: #fff; }

    /* Buttons */
    .stButton>button {
        border: 2px solid #feda4a;
        background-color: #feda4a;
        color: #000;
        padding: 10px 24px;
        border-radius: 5px;
        font-weight: bold;
        text-transform: uppercase;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #000;
        color: #feda4a;
    }

    /* Intro text */
    .intro-text {
        font-size: 1.2em;
        line-height: 1.6;
        text-align: center;
        transform: perspective(300px) rotateX(15deg);
        margin-bottom: 2em;
    }

    /* Animations */
    @keyframes twinkle {
      0%, 100% { opacity: 0.1; }
      50% { opacity: 0.2; }
    }

    /* Mobile-friendly */
    @media (max-width: 600px) {
      h1 {
        font-size: 2rem;
      }

      p {
        font-size: 1rem;
      }

      button {
        font-size: 0.9rem;
      }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="background-layer"></div>
        <div class="stars-layer"></div>
        <div class="aura-layer"></div>
        <div class="overlay-layer"></div>
    """, unsafe_allow_html=True)

# --- Language Content ---
content = {
    "ru": {
        "title": "Алишер & Ботагоз",
        "intro": "Давным-давно, в далекой-далекой галактике...",
        "header": "Приглашение на Свадьбу",
        "alliance": "С великой радостью приглашаем вас присоединиться к нашему альянсу!",
        "date": "06.09.2025",
        "time": "17:00",
        "address_intro": "Наша сага продолжится по адресу:",
        "address_placeholder": "Portofino. Проспект Туран, 27",
        "rsvp_intro": "Подтвердите свое присутствие до 20.08.2025",
        "form_name": "Ваше имя (Имена гостей)",
        "form_attendance": "Подтверждаете присутствие?",
        "option_yes": "Да, я присоединюсь к Альянсу",
        "option_no": "Нет, я на стороне Империи",
        "submit_button": "Отправить ответ",
        "thank_you": "Спасибо! Ваш ответ записан в голокрон.",
        "error_name": "Пожалуйста, введите ваше имя, юный падаван.",
        "countdown_text": "До нашей свадьбы осталось:",
        "days": "дней",
        "hours": "часов",
        "minutes": "минут",
        "wedding_started": "Свадьба началась!"
    },
    "kz": {
        "title": "Әлішер & Ботагоз",
        "intro": "Ерте, ерте заманда, алыс-алыс галактикада...",
        "header": "Үйлену тойына шақыру",
        "alliance": "Сіздерді біздің одағымыздың құрылу салтанатына шақырамыз!",
        "date": "06.09.2025",
        "time": "17:00",
        "address_intro": "Біздің дастанымыз мына мекен-жайда жалғасады:",
        "address_placeholder": "Portofino. Туран Даңғылы, 27",
        "rsvp_intro": "Қатысуыңызды 20.08.2025 дейін растаңыз",
        "form_name": "Сіздің есіміңіз (Қонақтардың есімдері)",
        "form_attendance": "Қатысуды растайсыз ба?",
        "option_yes": "Иә, мен Альянсқа қосыламын",
        "option_no": "Жоқ, мен Империя жағындамын",
        "submit_button": "Жауапты жіберу",
        "thank_you": "Рахмет! Сіздің жауабыңыз голокронға жазылды.",
        "error_name": "Есіміңізді енгізіңіз, жас падаван.",
        "countdown_text": "Тойымызға қалды:",
        "days": "күн",
        "hours": "сағат",
        "minutes": "минут",
        "wedding_started": "Той басталды!"
    }
}

# --- Main App Logic ---
load_css()

# Wedding Date for Countdown
wedding_date = datetime.datetime(2025, 9, 6, 17, 0)

def get_countdown(wedding_date, lang_content):
    now = datetime.datetime.now()
    time_left = wedding_date - now

    if time_left.total_seconds() < 0:
        return lang_content["wedding_started"]
    else:
        days = time_left.days
        hours = time_left.seconds // 3600
        minutes = (time_left.seconds % 3600) // 60
        seconds = time_left.seconds % 60
        return f"{days} {lang_content["days"]}, {hours} {lang_content["hours"]}, {minutes} {lang_content["minutes"]}"

# Language Selection
lang_choice = st.sidebar.radio("Language / Тіл", ["Русский", "Қазақ"], label_visibility="collapsed")
lang = "ru" if lang_choice == "Русский" else "kz"

t = content[lang]

# --- Display Invitation Details ---
st.title(t["title"])
st.header(t["header"])
st.markdown(f'<p class="intro-text">{t["intro"]}</p>', unsafe_allow_html=True)
st.write(t["alliance"])
st.subheader(f'{t["date"]} | {t["time"]}')
st.write("") # Spacer
st.write(t["address_intro"])
st.info(t["address_placeholder"])
st.write("") # Spacer

# --- Countdown ---
st.subheader(t["countdown_text"])
st.write(get_countdown(wedding_date, t))
st.write("") # Spacer

# --- RSVP Form ---
st.header(t["rsvp_intro"])

if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

if st.session_state.form_submitted:
    st.success(t["thank_you"])
else:
    with st.form(key='rsvp_form'):
        guest_name = st.text_input(label=t["form_name"])
        attendance = st.radio(
            label=t["form_attendance"],
            options=[t["option_yes"], t["option_no"]],
            index=0
        )
        submitted = st.form_submit_button(label=t["submit_button"])

        if submitted:
            if not guest_name.strip():
                st.error(t["error_name"])
            else:
                try:
                    response_data = pd.DataFrame([{{
                        "Name": guest_name.strip(),
                        "Attendance": attendance,
                        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }}])

                    if not os.path.exists(RSVP_FILE):
                        # Create the file with headers if it doesn't exist
                        pd.DataFrame(columns=["Name", "Attendance", "Timestamp"]).to_csv(RSVP_FILE, index=False)
                    response_data.to_csv(RSVP_FILE, mode='a', header=False, index=False)
                    
                    st.session_state.form_submitted = True
                    st.rerun()

                except Exception as e:
                    st.error(f"An error occurred: {{e}}")
                    st.exception(e)
