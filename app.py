import streamlit as st
import pandas as pd
import os
import base64
import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Бота & Алишер",
    page_icon="💍",
    layout="centered" 
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
    encoded_image = get_base64_of_bin_file("background.png")
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Russo+One&display=swap');
    /* Background and layout */
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        position: relative;
        overflow: hidden;
        font-family: 'Inter', sans-serif;
        text-align: center;
    }}
    
    .stApp > * {{
        position: relative;
        z-index: 1;
    }}

    .stApp > header {{ 
        background-color: transparent; 
    }}

    /* Main content block */
    .main .block-container {{
        background-color: rgba(0, 0, 0, 0.85);
        border: 2px solid #FFD700;
        box-shadow: 0 0 30px 10px #FFD700;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
    }}

    /* Typography */
    h1 {{
        color: #FFD700 !important;
        text-shadow: 0 0 8px #000, 0 0 16px #000;
        font-weight: 800;
        font-size: 2.3em;
        margin-top: 24px;
        letter-spacing: 0.04em;
        font-family: 'Russo One', sans-serif !important;
    }}

    h2 {{
        color: #FFD700 !important;
        text-shadow: 0 0 5px #000, 0 0 10px #000;
        font-weight: 500;
        font-size: 1.75em;
        font-family: 'Russo One', sans-serif !important;
    }}
    
    names {{
        color: #ffffff !important;
        text-shadow: 0 0 5px #000, 0 0 10px #000;
        font-weight: 500;
        font-size: 1.75em;
        font-family: 'Russo One', sans-serif !important;
    }}

    h3, label, .st-emotion-cache-16txtl3 {{
        color: #FFD700 !important;
        text-shadow: 0 0 5px #000, 0 0 10px #000;
        font-size: 1.1em;
        font-family: 'Russo One', sans-serif !important;
    }}

    /* Markdown text */
    .main .block-container p {{
        color: #FFD700;
        text-shadow: 0 0 5px #000, 0 0 10px #000;
        font-size: 1.3em; 
    }}
    p {{
        color: #FFD700;
        font-size: 1.2em !important;
    }}

    /* Buttons */
    .stButton>button {{
        border: 2px solid #FFD700;
        background-color: #FFD700;
        color: #000;
        padding: 12px 24px;
        border-radius: 6px;
        font-weight: bold;
        text-transform: uppercase;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 0 10px #FFD700;
    }}

    .stButton>button:hover {{
        background-color: #000;
        color: #FFD700;
        box-shadow: 0 0 20px #FFD700;
    }}

    /* Centering Streamlit info blocks */
    .st-emotion-cache-1c7y2kd {{
        text-align: center;
    }}

    /* Radio button labels */
    .stRadio label {{
        color: #FFD700 !important;
        font-weight: bold;
        text-shadow: 0 0 4px #000;
    }}

    /* Input fields */
    .stTextInput>div>div>input {{
        background-color: rgba(255, 255, 255, 0.05);
        color: #FFD700;
        border: 1px solid #FFD700;
        border-radius: 5px;
    }}

    .stTextInput>div>div>input::placeholder {{
        color: #ccc;
    }}
    </style>
    """, unsafe_allow_html=True)


# --- Language Content ---
content = {
    "ru": {
        "title": "Two hearts. One galaxy. Infinite adventures.",
        'subtitle': 'Наш семейный альянс рад сообщить:',
        'intro1': 'В галактике, не такой уж далёкой,',
        'intro2': 'скоро произойдёт объединение двух звёздных систем -',
        'intro3': 'нашей дочери Ботагоз и её избранного Алишера.',
        'address_intro': '🌌 Звездная точка встречи:',
        'address': "📍Ресторан Portofino, Астана. Проспект Туран, 27",
        'dresscode_intro': '👗 Дресс-код:',
        'dresscode_dark': 'Тёмные образы — для тех, кто выбирает силу и форму',
        'dresscode_light': 'Светлые — для тех, кто несёт свет и тепло',
        'dresscode_last': 'Главное — сияние в глазах и порядок в галактике',
        'invite': 'Приглашаем вас стать частью этого межгалактического события.',
        'final_message': 'Да пребудет с вами любовь. И хорошее настроение.',
        'farewell': 'С нетерпением ждём встречи, Нурлан и Сауле 💛',
        'date': "6 сентября 2025 года",
        'time': '17:00',
        'time_intro': '🕔 Время встречи',
       
        "rsvp_intro": "Подтвердите свое присутствие до 20 августа (еще не работает)",
        "form_name": "Ваше имя (Имена гостей)",
        "form_attendance": "Подтверждаете присутствие?",
        "option_yes": "Да, я присоединюсь к Альянсу",
        "option_no": "Нет, я на стороне Империи",
        "submit_button": "Отправить ответ",
        "thank_you": "Спасибо! Ваш ответ записан в голокрон.",
        "error_name": "Пожалуйста, введите ваше имя, юный падаван.",
        "countdown_text": "До нашего мероприятия осталось:",
        "days": "дней",
        "hours": "часов",
        "minutes": "минут",
        "wedding_started": "Свадьба началась!",
    },

    "kz": {
        "title": "Үйлену тойына шақыру",
        "intro1": 'Екі жұлдыз тағдыр орбитасында тоғысқанда - жаңа әлем дүниеге келеді.',
        'intro2': '💫Күш - махаббат, ал жол біреу - бірге.💫',
        "header": "Ботагоз бен Алишер",
        "alliance": '''сіздерді өздерінің ғаламдары біртұтас болатын күнді бірге өткізуге шақырады.''',
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

# --- Landing Page Logic ---
def show_landing_page():
    # Use background.png as background
    encoded_bg = get_base64_of_bin_file("background.png")
    st.markdown(f"""
    <style>
    .landing-bg {{
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-image: url('data:image/png;base64,{encoded_bg}');
        background-size: cover;
        background-position: center;
        z-index: 0;
    }}
    .center-btn {{
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 2;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}
    .landing-btn-container button {{
        background: #FFD700;
        color: #000;
        border: 2px solid #FFD700;
        border-radius: 6px;
        font-weight: bold;
        font-size: 1.1em;
        padding: 10px 32px;
        box-shadow: 0 0 10px #FFD700;
        cursor: pointer;
        transition: all 0.2s;
    }}
    .landing-btn-container button:hover {{
        background: #000;
        color: #FFD700;
        box-shadow: 0 0 20px #FFD700;
    }}
    </style>
    <div class="landing-bg"></div>
    <div class="center-btn">
        <div class="landing-btn-container" id="landing-btn-anchor"></div>
    </div>
    """, unsafe_allow_html=True)
    # Place the button using Streamlit (centered)
    st.markdown("<div style='height: 120px'></div>", unsafe_allow_html=True)  # Spacer for Streamlit layout
    btn_placeholder = st.empty()
    with btn_placeholder.container():
        btn_clicked = st.button("Продолжить / Continue", key="continue_btn", help="Открыть приглашение")
    if btn_clicked:
        st.session_state.landing_done = True
        st.rerun()

# --- Main App Routing ---
if "landing_done" not in st.session_state:
    st.session_state.landing_done = False

if not st.session_state.landing_done:
    show_landing_page()
    st.stop()

# --- Main App Logic ---
load_css()

# Add custom CSS for glowing background block behind main text
block_glow_css = """
<style>
.glow-block {
    display: block;
    width: 720px;
    max-width: 95vw;
    margin: 18px auto 18px auto;
    background: rgba(0,0,0,0.85);
    border-radius: 18px;
    box-shadow: 0 0 32px 8px #FFD70099, 0 0 0 4px #FFD70044;
    padding: 18px 32px 14px 32px;
    border: 2px solid #FFD700;
    text-align: center;
}
.glow-block h1, .glow-block names, .glow-block p {
    color: #FFD700 !important;
    text-shadow: none !important;
    font-family: 'Russo One', sans-serif !important;
    margin: 0 0 8px 0;
}
</style>
"""
st.markdown(block_glow_css, unsafe_allow_html=True)

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

#stars 
st.markdown("""
<style>
.glimmer-stars {
  pointer-events: none;
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  z-index: 9999;
  overflow: hidden;
}
.glimmer-stars span {
  position: absolute;
  font-size: 6px;
  color: #FFD700;
  opacity: 0.4;
  animation: glimmer 2.5s infinite;
  text-shadow: 0 0 8px #FFD700, 0 0 16px #fff;
}
/* Corners */
.glimmer-stars span:nth-child(1) { left: 22vw; top: 2vh; animation-delay: 0s; }
.glimmer-stars span:nth-child(2) { left: 97vw; top: 5vh; animation-delay: 0.5s; }
.glimmer-stars span:nth-child(3) { left: 2vw; top: 97vh; animation-delay: 1s; }
.glimmer-stars span:nth-child(4) { left: 97vw; top: 97vh; animation-delay: 1.5s; }
/* Top and bottom edges */
.glimmer-stars span:nth-child(7) { left: 60vw; top: 8vh; animation-delay: 1.2s; }
.glimmer-stars span:nth-child(8) { left: 80vw; top: 3vh; animation-delay: 1.7s; }
.glimmer-stars span:nth-child(11) { left: 60vw; top: 98vh; animation-delay: 1.4s; }
.glimmer-stars span:nth-child(12) { left: 80vw; top: 98vh; animation-delay: 1.9s; }
/* Left and right edges */
.glimmer-stars span:nth-child(13) { left: 24vw; top: 20vh; animation-delay: 0.3s; }
.glimmer-stars span:nth-child(14) { left: 20vw; top: 40vh; animation-delay: 0.8s; }
.glimmer-stars span:nth-child(15) { left: 30vw; top: 60vh; animation-delay: 1.3s; }
.glimmer-stars span:nth-child(17) { left: 85vw; top: 20vh; animation-delay: 0.6s; }
.glimmer-stars span:nth-child(18) { left: 88vw; top: 40vh; animation-delay: 1.1s; }
.glimmer-stars span:nth-child(20) { left: 93vw; top: 80vh; animation-delay: 2.1s; }

@keyframes glimmer {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}
</style>
<div class="glimmer-stars">
  <span>★</span><span>★</span><span>★</span><span>★</span>
  <span>★</span><span>★</span><span>★</span><span>★</span>
  <span>★</span><span>★</span><span>★</span><span>★</span>
  <span>★</span><span>★</span><span>★</span><span>★</span>
  <span>★</span><span>★</span><span>★</span><span>★</span>
</div>
""", unsafe_allow_html=True)

# --- Display Invitation Details ---

st.markdown(f'<h1>{t["title"]}</h1>', unsafe_allow_html=True)

st.markdown("""
<div class='glow-block'>
    <p>{intro1}</p>
    <p>{intro2}</p>
    <h2>{intro3}</h2>
</div>
""".format(intro1=t['intro1'], intro2=t['intro2'], intro3=t['intro3']), unsafe_allow_html=True)

st.markdown("""
<div class='glow-block'>
    <p>{address_intro}</p>
    <p>{address}</p>
    <p>{time_intro}</p>
    <p>{date} | {time}</p>
</div>
""".format(address_intro=t['address_intro'], address=t['address'], time_intro=t['time_intro'], date=t['date'], time=t['time']), unsafe_allow_html=True)

st.markdown("""
<div class='glow-block'>
    <p>{dresscode_intro}</p>
    <p>{dresscode_dark}</p>
    <p>{dresscode_light}</p>
    <p>{dresscode_last}</p>
</div>
""".format(dresscode_intro=t['dresscode_intro'], dresscode_dark=t['dresscode_dark'], dresscode_light=t['dresscode_light'], dresscode_last=t['dresscode_last']), unsafe_allow_html=True)


# --- Countdown & Final Message ---
st.write("")
st.subheader(f"⏳ {t['countdown_text']}")
st.markdown(f"<h2 style='color:#FFD700'>{get_countdown(wedding_date, t)}</h2>", unsafe_allow_html=True)
st.write("")
st.markdown(f"<h3>{t['final_message']}</h3>", unsafe_allow_html=True)
st.markdown(f"<h3><b>{t['farewell']}</b></h3>", unsafe_allow_html=True)

st.write("")  # Spacer
st.markdown("---")

# --- RSVP Form ---
st.header(t["rsvp_intro"])

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if st.session_state.form_submitted:
    st.success(t["thank_you"])
else:
    with st.form(key="rsvp_form"):
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
                    response_data = pd.DataFrame([{
                        "Name": guest_name.strip(),
                        "Attendance": attendance,
                        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }])

                    if not os.path.exists(RSVP_FILE):
                        pd.DataFrame(columns=["Name", "Attendance", "Timestamp"]).to_csv(RSVP_FILE, index=False)

                    response_data.to_csv(RSVP_FILE, mode="a", header=False, index=False)

                    st.session_state.form_submitted = True
                    st.rerun()

                except Exception as e:
                    st.error(f"Произошла ошибка: {e}")
                    st.exception(e)

