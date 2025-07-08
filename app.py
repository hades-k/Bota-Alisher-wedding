import streamlit as st
import pandas as pd
import os
import base64
import datetime
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Бота & Алишер",
    page_icon="💍",
    layout="wide"
)

# --- File for RSVPs ---
RSVP_FILE = "rsvps.csv"

# --- Function to get base64 encoded image for CSS ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- Load Custom CSS for Star Wars Theme ---
def load_css():
    background_image_path = "background.png"
    if os.path.exists(background_image_path):
        encoded_image = get_base64_of_bin_file(background_image_path)
        background_style = f"background-image: url(data:image/png;base64,{encoded_image});"
    else:
        background_style = "background-color: #000;"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    .stApp {{
        {background_style}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp > header {{ 
        background-color: transparent; 
    }}
    .main .block-container {{
        background-color: rgba(0, 0, 0, 0.75);
        border: 2px solid #feda4a;
        box-shadow: 0 0 20px #feda4a;
        padding: 2rem;
        border-radius: 10px;
        max-width: 700px;
        margin: auto;
        text-align: center;
    }}
    h1, h2, h3, p, label {{
        font-family: 'Orbitron', sans-serif;
        color: #feda4a;
    }}
    h1 {{ text-transform: uppercase; }}
    h2 {{ color: #fff; }}
    .stButton>button {{
        border: 2px solid #feda4a;
        background-color: #feda4a;
        color: #000;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        text-transform: uppercase;
    }}
    .stButton>button:hover {{
        background-color: #000;
        color: #feda4a;
    }}
    .intro-text {{
        font-size: 1.2em;
        line-height: 1.6;
        text-align: center;
        transform: perspective(300px) rotateX(15deg);
        margin-bottom: 2em;
    }}
    .countdown-box {{
        display: inline-block;
        background: rgba(0,0,0,0.5);
        border-radius: 5px;
        padding: 10px;
        margin: 5px;
        min-width: 80px;
    }}
    .countdown-number {{ font-size: 2em; font-weight: bold; color: #fff; }}
    .countdown-label {{ font-size: 0.8em; color: #feda4a; }}
    </style>
    """, unsafe_allow_html=True)

# --- Language Content ---
content = {
    "ru": {
        "title": "Ботагоз & Алишер",
        "intro": "Давным-давно, в далекой-далекой галактике...",
        "header": "Приглашение на Свадьбу",
        "alliance": "С великой радостью приглашаем вас присоединиться к нашему альянсу!",
        "date": "06.09.2025",
        "time": "17:00",
        "countdown_header": "До начала саги осталось:",
        "days": "Дней", "hours": "Часов", "minutes": "Минут", "seconds": "Секунд",
        "celebration_started": "Да пребудет с вами Сила! Праздник начался!",
        "address_intro": "Наша сага продолжится по адресу:",
        "address_placeholder": "Portofino. Проспект Туран, 27",
        "rsvp_intro": "Подтвердите свое присутствие до 20.08.2025",
        "form_name": "Ваше имя (Имена гостей)",
        "form_attendance": "Подтверждаете присутствие?",
        "option_yes": "Да, я присоединюсь к Альянсу",
        "option_no": "Нет, я на стороне Империи",
        "submit_button": "Отправить ответ",
        "thank_you": "Спасибо! Ваш ответ записан в голокрон.",
        "error_name": "Пожалуйста, введите ваше имя, юный падаван."
    },
    "kz": {
        "title": "Ботагөз & Әлішер",
        "intro": "Ерте, ерте заманда, алыс-алыс галактикада...",
        "header": "Үйлену тойына шақыру",
        "alliance": "Сіздерді біздің одағымыздың құрылу салтанатына шақырамыз!",
        "date": "06.09.2025",
        "time": "17:00",
        "countdown_header": "Дастанның басталуына қалды:",
        "days": "Күн", "hours": "Сағат", "minutes": "Минут", "seconds": "Секунд",
        "celebration_started": "Күш сізбен бірге болсын! Мереке басталды!",
        "address_intro": "Біздің дастанымыз мына мекен-жайда жалғасады:",
        "address_placeholder": "Portofino. Туран Даңғылы, 27",
        "rsvp_intro": "Қатысуыңызды 20.08.2025 дейін растаңыз",
        "form_name": "Сіздің есіміңіз (Қонақтардың есімдері)",
        "form_attendance": "Қатысуды растайсыз ба?",
        "option_yes": "Иә, мен Альянсқа қосыламын",
        "option_no": "Жоқ, мен Империя жағындамын",
        "submit_button": "Жауапты жіберу",
        "thank_you": "Рахмет! Сіздің жауабыңыз голокронға жазылды.",
        "error_name": "Есіміңізді енгізіңіз, жас падаван."
    }
}

# --- Main App ---
load_css()

# Language Selection
lang_choice = st.sidebar.radio("Language / Тіл", ["Русский", "Қазақ"], label_visibility="collapsed")
lang = "ru" if lang_choice == "Русский" else "kz"

t = content[lang]

st.title(t["title"])
st.header(t["header"])

st.markdown(f'<p class="intro-text">{t["intro"]}</p>', unsafe_allow_html=True)
st.write(t["alliance"])
st.subheader(f'{t["date"]} | {t["time"]}')

# Countdown Timer
st.write(f'### {t["countdown_header"]}')
countdown_placeholder = st.empty()

def run_countdown():
    wedding_dt = datetime.datetime(2025, 9, 6, 17, 0, 0)
    while True:
        now = datetime.datetime.now()
        delta = wedding_dt - now
        if delta.total_seconds() > 0:
            days, remainder = divmod(delta.seconds, 86400)
            days = delta.days
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            countdown_placeholder.markdown(f"""
            <div style="display: flex; justify-content: center;">
                <div class="countdown-box"><div class="countdown-number">{days}</div><div class="countdown-label">{t['days']}</div></div>
                <div class="countdown-box"><div class="countdown-number">{hours}</div><div class="countdown-label">{t['hours']}</div></div>
                <div class="countdown-box"><div class="countdown-number">{minutes}</div><div class="countdown-label">{t['minutes']}</div></div>
                <div class="countdown-box"><div class="countdown-number">{seconds}</div><div class="countdown-label">{t['seconds']}</div></div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
        else:
            countdown_placeholder.header(t["celebration_started"])
            break

run_countdown()

st.write("") # Spacer
st.write(t["address_intro"])
st.info(t["address_placeholder"])

st.header(t["rsvp_intro"])

with st.form(key="rsvp_form"):
    guest_name = st.text_input(label=t["form_name"])
    attendance = st.radio(
        label=t["form_attendance"],
        options=[t["option_yes"], t["option_no"]],
        index=0
    )
    submitted = st.form_submit_button(label=t["submit_button"])

    if submitted:
        if not guest_name:
            st.error(t["error_name"])
        else:
            new_data = pd.DataFrame([[guest_name, attendance]])
            if not os.path.exists(RSVP_FILE):
                new_data.to_csv(RSVP_FILE, index=False, header=["Name", "Attendance"])
            else:
                new_data.to_csv(RSVP_FILE, mode='a', header=False, index=False)
            
            st.success(t["thank_you"])