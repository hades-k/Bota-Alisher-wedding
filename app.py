import streamlit as st
import pandas as pd
import os
import base64
import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Бота & Алишер",
    page_icon="💍",
    layout="centered" # Use centered layout for better focus
)

# --- File for RSVPs ---
RSVP_FILE = "rsvps.csv"

# --- Function to get base64 encoded image for CSS ---
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# --- Load Custom CSS for Star Wars Theme ---
def load_css():
    st.markdown(f"""
    <style>
    .stApp {
        background-color: #000;
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        position: relative;
        overflow: hidden;
    }

    /* Dark overlay to improve readability */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.4);
        z-index: 0;
    }
    .stApp > * {
        position: relative;
        z-index: 1;
    }


    .stApp > header { 
        background-color: transparent; 
    }

    /* Main container styling */
    .main .block-container {
        background-color: rgba(0, 0, 0, 0.85);
        border: 2px solid #FFD700;
        box-shadow: 0 0 30px 10px #FFD700;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
    }

    /* Typography */
    h1 {
        color: #FFD700;
        text-shadow: 0 0 5px #000, 0 0 10px #000;
        font-weight: 800; /* Extra Bold */
        margin-top: 24px; /* Top padding */
    }
    h2 {
        color: #FFD700; /* Changed from #fff for consistency */
        text-shadow: 0 0 5px #000, 0 0 10px #000;
        font-weight: 400; /* Normal */
    }
    h3, p, label, .st-emotion-cache-16txtl3 {
        color: #FFD700; /* Changed from #feda4a for contrast */
        text-shadow: 0 0 5px #000, 0 0 10px #000;
    }

    /* Buttons */
    .stButton>button {
        border: 2px solid #FFD700;
        background-color: #FFD700;
        color: #000;
        padding: 10px 24px;
        border-radius: 5px;
        font-weight: bold;
        text-transform: uppercase;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #000;
        color: #FFD700;
    }

    /* Intro text */
    .intro-text {
        font-size: 1.2em;
        line-height: 1.6;
        text-align: center;
        transform: perspective(300px) rotateX(15deg);
        margin-bottom: 2em;
        font-weight: 300; /* Light */
        font-style: italic;
    }

    /* st.info alignment */
    .st-emotion-cache-1c7y2kd {
        text-align: center;
    }

    /* Optional: Animated starfield background (commented out)
    .stApp::after {
        content: "";
        position: fixed;
        top: 0; left: 0;
        width: 100%;
        height: 100%;
        background: url('https://raw.githubusercontent.com/Julian-Nash/starfield-animation/main/starfield-bg.gif') repeat;
        background-size: cover;
        opacity: 0.08;
        z-index: -2;
        animation: drift 60s linear infinite;
    }}
    @keyframes drift {
        from { background-position: 0 0; }
        to { background-position: 10000px 0; }
    }}
    */

    </style>
    """
    """, unsafe_allow_html=True)

# --- Language Content ---
content = {
    "ru": {
        "title": "Приглашение на свадьбу",
        "intro": """Когда две звезды пересекаются на орбите судьбы —
рождается новый мир.
Мир, в котором сила — это любовь,
а путь один — вместе.""",
        "header": "С большой радостью",
        "alliance": """<h2>Ботагоз и Алишер</h2>
приглашают вас разделить с ними день,
в который их вселенные станут одним целым."""
        "date": "6 сентября 2025 года",
        "time": "17:00",
        "address_intro": "Ресторан Portofino, Астана. Проспект Туран, 27",
        "address_placeholder": "Дресс-код: торжественный, с лёгким сиянием ✨",
        "rsvp_intro": "Подтвердите свое присудствие до 20 августа",
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
        "wedding_started": "Свадьба началась!",
        "final_message": "Да пребудет с вами… праздник."
    },
    "kz": {
        "title": "Үйлену тойына шақыру",
        "intro": """Екі жұлдыз тағдыр орбитасында тоғысқанда —
жаңа әлем дүниеге келеді.
Күш — махаббат,
ал жол біреу — бірге.""",
        "header": "Үлкен қуанышпен",
        alliance": """<h2>Ботагөз бен Әлішер</h2>
сіздерді өздерінің ғаламдары біртұтас болатын күнді
бірге өткізуге шақырады.""",

        "date": "2025 жылғы 6 қыркүйек",
        "time": "17:00",
        "address_intro": "Portofino мейрамханасы, Астана. Тұран даңғылы, 27",
        "address_placeholder": "Дресс-код: салтанатты, жеңіл жарқыраған ✨",
        "rsvp_intro": "Қатысуыңызды 20 тамызға дейін растаңыз",
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
        "wedding_started": "Той басталды!",
        "final_message": "Сізбен бірге... мереке болсын."
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
st.header(t["title"])
st.subheader(t["header"])
st.markdown(f'<p class="intro-text">{t["intro"]}</p>', unsafe_allow_html=True)
st.write(t["alliance"])
st.subheader(f'{t["date"]} | {t["time"]}')
st.write("") # Spacer
st.write(t["address_intro"])
st.write(t["address_placeholder"])
st.write("") # Spacer

st.subheader(t["countdown_text"])
st.write(get_countdown(wedding_date, t))
st.write("") # Spacer

st.subheader(t["final_message"])

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
