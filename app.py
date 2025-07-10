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
    encoded_image = get_base64_of_bin_file("background-1.png")
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
    
    .glow-block {{
        display: block;
        width: 720px;
        max-width: 95vw;
        margin: 18px auto 18px auto;
        background: rgba(0,0,0,0.75);
        border-radius: 18px;
        box-shadow: 0 0 18px 7px #FFD70099, 0 0 0 4px #FFD70044;
        padding: 12px 25px 12px 25px;
        border: 2px solid #FFD700;
        text-align: center;
    }}   
    
    .glow-block h1, .glow-block names, .glow-block p {{
        color: #FFD700 !important;
        text-shadow: none !important;
        font-family: 'Russo One', sans-serif !important;
        margin: 0 0 8px 0;
    }}
    
    .stCheckbox > div > label {{
    color: #FFD700 !important;
    text-shadow: 1px 1px 2px #000 !important;
    font-size: 1.1em;
    font-weight: 500;
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
        'intro3': 'нашей дочери',
        'bo': 'Ботагоз',
        'intro4': 'и её избранного',
        'ali': 'Алишера',
        'address_intro': '🌌 Звездная точка встречи:',
        'address': "📍Ресторан Portofino, Астана. Проспект Туран, 27",
        'dresscode_intro': '👗 Дресс-код:',
        'dresscode': 'Вечерний стиль с космическими акцентами',
        'invite': 'Приглашаем вас стать частью этого межгалактического события.',
        'final_message': 'Да пребудет с вами любовь. И хорошее настроение.',
        'farewell': 'С нетерпением ждём встречи,',
        'farewell_names': 'Нурлан и Сауле',
        'date': "6 сентября 2025 года",
        'time': '17:00',
        'time_intro': '🕔 Время прибытия',
        "rsvp_intro": "Подтвердите свое присутствие до 20 августа (еще не работает)",
        "submit_button": "Отправить ответ",
        "thank_you": "Спасибо! Ваш ответ записан в голокрон.",
        "countdown_text": "⏳До нашего мероприятия осталось:",
        "days": "дней",
        "hours": "часов",
        "minutes": "минут",
        "wedding_started": "Праздник началась!",
        "rsvp_question": "Дорогие гости, подтверждаете присутствие?",
        "rsvp_yes_1": "Да, 1",
        "rsvp_yes_2": "Да, 2",
        "rsvp_no": "Нет",
    },

    "kz": {
        "title": "Two hearts. One galaxy. Infinite adventures.",
        'subtitle': 'Біздің отбасылық одақ қуана хабарлайды:',
        'intro1': 'Алыс емес бір галактикада',
        'intro2': 'жұлдызды екі жүйенің қосылуы орын алмақ -',
        'intro3': 'қызымыз',
        'bo': 'Ботагоз',
        'intro4': 'және оның таңдағаны',
        'ali': 'Алишер',
        'address_intro': '🌌 Жұлдызды кездесу орыны:',
        'address': "📍Астана қаласы, Тұран даңғылы 27, «Portofino» мейрамханасы",
        'dresscode_intro': '👗 Дресс-код:',
        'dresscode': 'Ғарыштық екпіндері бар кешкі стиль',
        'invite': 'Сізді осы галактаралық оқиғаның бір бөлігі болуға шақырамыз.',
        'final_message': 'Сүйіспеншілік пен көтеріңкі көңіл сізбен бірге болсын.',
        'farewell': 'Кездескенше асыға күтеміз,',
        'farewell_names': 'Нұрлан - Сауле',
        'date': "2025 ж. 6 қыркүйек",
        'time': 'сағат 17:00',
        'time_intro': '🕔 Келу уақыты:',
        "rsvp_intro": "Қатысуыңызды 20 тамызға дейін растаңыз (әлі жұмыс істемейді)",
        "submit_button": "Жауапты жіберу",
        "thank_you": "Рахмет! Сіздің жауабыңыз голокронға жазылды.",
        "countdown_text": "⏳Тойымызға қалды:",
        "days": "күн",
        "hours": "сағат",
        "minutes": "минут",
        "wedding_started": "Мереке басталды!",
        "rsvp_question": "Құрметті қонақтар, қатысатыныңызды растайсыз ба?",
        "rsvp_yes_1": "Иә, 1",
        "rsvp_yes_2": "Иә, 2",
        "rsvp_no": "Жоқ",
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

st.markdown(f'<h1>{t["title"]}</h1>', unsafe_allow_html=True)

st.markdown(f""" <div class='glow-block'>
    <p> {t['intro1']} </p>
    <p> {t['intro2']} </p>
    <h2> {t['intro3']} <span style="color:white"> {t['bo']} </span> {t['intro4']} <span style="color:white"> {t['ali']} </span> </h2>
</div>
""", unsafe_allow_html=True)

st.markdown(f""" <div class='glow-block'>
    <p>{t['address_intro']}</p>
    <p>{t['address']}</p>
    <p>{t['time_intro']}</p>
    <p>{t['date']} | {t['time']}</p>
</div> """, unsafe_allow_html=True)

st.markdown(f""" <div class='glow-block'>
    <p>{t['dresscode_intro']}</p>
    <p>{t['dresscode']}</p>
</div> """, unsafe_allow_html=True)

st.write("")  # Spacer

# --- RSVP Form --- (complete fail)
st.header(t["rsvp_intro"])

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if st.session_state.form_submitted:
    st.success(t["thank_you"])
else:
    with st.markdown("""<div class="glow-block">""", unsafe_allow_html=True):
        with st.form(key="rsvp_form"):
            attendance = st.radio(
                label=t['rsvp_question'],
                options=[t['rsvp_yes_1'], t['rsvp_yes_2'], t['rsvp_no']],
                index=None,
                key="attendance_radio")
            submitted = st.form_submit_button(label=t["submit_button"])
            if submitted:
                if attendance is not None:
                    guest_name = "Anonymous"
                    try:
                        response_data = pd.DataFrame([{
                            "Name": guest_name,
                            "Attendance": attendance,
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}])
                        if not os.path.exists(RSVP_FILE):
                            pd.DataFrame(columns=["Name", "Attendance", "Timestamp"]).to_csv(RSVP_FILE, index=False)
                        response_data.to_csv(RSVP_FILE, mode="a", header=False, index=False)
                        st.session_state.form_submitted = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"Произошла ошибка: {e}")
                        st.exception(e)
                else:
                    st.warning("Пожалуйста, выберите один из вариантов")


    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

st.markdown(f""" <div class='glow-block'>
    <h3>{t['countdown_text']}</h3>
    <h3>{get_countdown(wedding_date, t)}</h3>
</div> """, unsafe_allow_html=True)

st.markdown(f""" <div class='glow-block'>
    <h3>{t['final_message']}
    <h3>{t['farewell']}</h3>
    <h2> <span style="color:white"> {t['farewell_names']} </span> </h2>
</div> """, unsafe_allow_html=True)
