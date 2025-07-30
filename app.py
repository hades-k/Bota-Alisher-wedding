import streamlit as st
import pandas as pd
import base64
import datetime
import gspread
from google.oauth2.service_account import Credentials

# --- Page Configuration ---
st.set_page_config(
    page_title="Бота & Алишер",
    page_icon="💍",
    layout="centered"
)

# --- Google Sheets Connection ---
# Function to create a gspread client from Streamlit secrets
def get_gspread_client():
    creds_dict = {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"],
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"],
    }
    credentials = Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    return gspread.authorize(credentials)

# Function to verify the code and get guest data
def verify_code(code):
    try:
        client = get_gspread_client()
        spreadsheet = client.open_by_url(st.secrets["gcp_spreadsheet_url"])
        sheet = spreadsheet.worksheet("guests")

        cell = sheet.find(code)
        if cell:
            row_values = sheet.row_values(cell.row)
            guest_data = {
                "row_index": cell.row,
                "code": row_values[0],
                "name": row_values[1],
                "status": row_values[2],
                "guest_count": int(row_values[3]) if len(row_values) > 3 and row_values[3].isdigit() else 0,
            }
            return guest_data
        else:
            return None
    except gspread.exceptions.SpreadsheetNotFound:
        st.error("Spreadsheet not found. Check the URL in your secrets.")
        return None
    except Exception as e:
        st.error(f"An error occurred while accessing the spreadsheet: {e}")
        return None

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
        background-repeat: no-repeat;
        background-size: cover;
        background-position: center center;
        background-attachment: scroll;
        font-family: 'Inter', sans-serif;
        text-align: center;
        position: relative;
        overflow-x: hidden;
    }}

    .stApp > * {{
        position: relative;
        z-index: 1;
    }}

    .stApp > header {{
        background-color: transparent;
    }}

    /* Typography */
    h1 {{
        color: #FFD700 !important;
        text-shadow: 0 0 8px #000, 0 0 16px #000;
        font-weight: 800;
        font-size: 2.2em;
        margin-top: 24px;
        letter-spacing: 0.04em;
        font-family: 'Russo One', sans-serif !important;
    }}

    h2 {{
        color: #FFD700 !important;
        text-shadow: 0 0 5px #000, 0 0 10px #000;
        font-weight: 500;
        font-size: 1.6em;
        font-family: 'Russo One', sans-serif !important;
    }}

    h3, label, .st-emotion-cache-16txtl3 {{
        color: #FFD700 !important;
        text-shadow: 0 0 5px #000, 0 0 10px #000;
        font-size: 1.4em !important;
        font-family: 'Russo One', sans-serif !important;
    }}

    /* Markdown text */
    .main .block-container p {{
        color: #FFD700;
        text-shadow: 0 0 5px #000, 0 0 10px #000;
        font-size: 1.2em;
    }}

    p {{
        color: #FFD700;
        font-size: 1.15em !important;
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
        text-align: center;
        font-size: 1.5em;
    }}

    .stTextInput>div>div>input::placeholder {{
        color: #ccc;
    }}

    .glow-block {{
    width: 100%;
    max-width: 720px;
    margin: 18px auto;
    background: rgba(0,0,0,0.4);
    border-radius: 18px;
    box-shadow: 0 0 18px 7px #FFD70099, 0 0 0 4px #FFD70044;
    padding: 12px 25px;
    border: 2px solid #FFD700;
    text-align: center;
    box-sizing: border-box;
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
        'farewell_names': 'Нурлан - Сауле',
        'date': "6 сентября 2025 года",
        'time': '17:00',
        'time_intro': '🕔 Время прибытия',
        "rsvp_intro": "Подтвердите свое присутствие",
        "submit_button": "Отправить ответ",
        "thank_you": "Спасибо! Ваш ответ записан в голокрон.",
        "countdown_text": "⏳До нашего мероприятия осталось:",
        'countdown_2':'✨✨✨',
        "days": "дней",
        "hours": "часов",
        "minutes": "минут",
        "wedding_started": "Праздник начался!",
        "rsvp_question": "подтверждаете присутствие?",
        "rsvp_yes_1": "Да, я приду один(а)",
        "rsvp_yes_2": "Да, мы придем вдвоем",
        "rsvp_no": "Нет, я не смогу присутствовать",
    },

    "kz": {
        "title": "Two hearts. One galaxy. Infinite adventures.",
        'subtitle': 'Біздің отбасылық одақ қуана хабарлайды:',
        'intro1': 'Алыс емес бір галактикада',
        'intro2': 'жұлдызды екі жүйенің қосылуы орын алмақ -',
        'intro3': 'қызымыз',
        'bo': 'Ботагөз',
        'intro4': 'және оның таңдағаны',
        'ali': 'Әлішер',
        'address_intro': '🌌 Жұлдызды кездесу орыны:',
        'address': "📍Астана қаласы, Тұран даңғылы 27, «Portofino» мейрамханасы",
        'dresscode_intro': '👗 Дресс-код:',
        'dresscode': 'Ғарыштық екпіндері бар кешкі стиль',
        'invite': 'Сізді осы галактаралық оқиғаның бір бөлігі болуға шақырамыз.',
        'final_message': 'Сүйіспеншілік пен көтеріңкі көңіл сізбен бірге болсын.',
        'farewell': 'Кездескенше асыға күтеміз,',
        'farewell_names': 'Нұрлан - Сәуле',
        'date': "2025 ж. 6 қыркүйек",
        'time': 'сағат 17:00',
        'time_intro': '🕔 Келу уақыты:',
        "rsvp_intro": "Қатысуыңызды растаңыз",
        "submit_button": "Жауапты жіберу",
        "thank_you": "Рахмет! Сіздің жауабыңыз голокронға жазылды.",
        "countdown_text": "⏳Тойымызға",
        'countdown_2': 'қалды',
        "days": "күн",
        "hours": "сағат",
        "minutes": "минут",
        "wedding_started": "Мереке басталды!",
        "rsvp_question": "қатысатыныңызды растайсыз ба?",
        "rsvp_yes_1": "Иә, мен жалғыз келемін",
        "rsvp_yes_2": "Иә, біз екеуміз келеміз",
        "rsvp_no": "Жоқ, келе алмаймын"
    }
}

# --- Landing Page Logic ---
def show_landing_page():
    encoded_bg = get_base64_of_bin_file("background-1.png")
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Russo+One&display=swap');
    .landing-bg {{
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-image: url('data:image/png;base64,{encoded_bg}');
        background-size: cover;
        background-position: center;
        z-index: 0;
    }}
    .top-landing-content {{
        position: relative;
        z-index: 2;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        width: 100%;
        max-width: 600px;
        margin: 2.5em auto 0 auto;
        box-sizing: border-box;
        padding: 0 1.5em;
    }}
    .landing-title {{
        font-family: 'Russo One', sans-serif;
        color: #FFD700;
        font-size: 3em;
        text-shadow: 0 2px 16px #000, 0 0 8px #FFD700;
        letter-spacing: 0.08em;
        margin-bottom: 1.2em;
        text-align: center;
        word-break: break-word;
        line-height: 1.1;
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
    }}
    .landing-instructions {{
        font-family: 'Russo One', sans-serif;
        color: #FFD700;
        font-size: 1.3em;
        text-shadow: 0 2px 8px #000, 0 0 4px #FFD700;
        margin-bottom: 2em;
        text-align: center;
        word-break: break-word;
        line-height: 1.2;
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
    }}
    .landing-form-wrapper {{
        width: 100%;
        max-width: 340px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-sizing: border-box;
    }}
    .stTextInput>div>div>input {{
        text-align: center;
        font-size: 2em;
        letter-spacing: 0.3em;
        background: rgba(255,255,255,0.85);
        border-radius: 8px;
        border: 2px solid #FFD700;
        color: #000;
        font-weight: bold;
        font-family: 'Russo One', sans-serif;
        width: 100%;
        box-sizing: border-box;
    }}
    .stTextInput>div>div>input::placeholder {{
        color: #FFD700;
        opacity: 0.7;
        font-family: 'Russo One', sans-serif;
    }}
    .stButton>button {{
        width: 100%;
        font-size: 1.3em;
        margin-top: 1.2em;
        background: #FFD700;
        color: #000;
        border: 2px solid #FFD700;
        border-radius: 6px;
        font-weight: bold;
        box-shadow: 0 0 10px #FFD700;
        transition: all 0.2s;
        font-family: 'Russo One', sans-serif;
        box-sizing: border-box;
    }}
    .stButton>button:hover {{
        background: #000;
        color: #FFD700;
        box-shadow: 0 0 20px #FFD700;
    }}
    </style>
    <div class="landing-bg"></div>
    <div class="top-landing-content">
        <div class="landing-title">Qyz Uzatu. Botagoz</div>
        <div class="landing-instructions">
            Пожалуйста, введите ваш 4-значный код<br>Сіздің 4 таңбалы кодты енгізіңіз
        </div>
        <div class="landing-form-wrapper">
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        code = st.text_input(
            "",
            max_chars=4,
            key="code_input",
            placeholder="****"
        )
        submitted = st.form_submit_button("Продолжить / Жалғастыру")

        if submitted:
            if code and code.isdigit() and len(code) == 4:
                guest_data = verify_code(code)
                if guest_data:
                    st.session_state.landing_done = True
                    st.session_state.guest_info = guest_data
                    st.rerun()
                else:
                    st.error("Код не найден / Код табылмады")
            else:
                st.warning("Пожалуйста, введите 4-значный код / 4 таңбалы кодты енгізіңіз")
    st.markdown("</div></div>", unsafe_allow_html=True)


# --- Main App Routing ---
if "landing_done" not in st.session_state:
    st.session_state.landing_done = False
if "guest_info" not in st.session_state:
    st.session_state.guest_info = None

if not st.session_state.landing_done or not st.session_state.guest_info:
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
        return f"{days} {lang_content['days']}, {hours} {lang_content['hours']}, {minutes} {lang_content['minutes']}"

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
</div>""", unsafe_allow_html=True)

st.markdown(f""" <div class='glow-block'>
    <p>{t['address_intro']}</p>
    <p>{t['address']}</p>
    <br>
    <p>{t['time_intro']}</p>
    <p>{t['date']} | {t['time']}</p>
    <br>
    <p>{t['dresscode_intro']}</p>
    <p>{t['dresscode']}</p>
</div>""", unsafe_allow_html=True)

st.write("")  # Spacer

# --- Function to update RSVP in Google Sheet ---
def update_rsvp(row_index, status, guest_count):
    try:
        client = get_gspread_client()
        spreadsheet = client.open_by_url(st.secrets["gcp_spreadsheet_url"])
        sheet = spreadsheet.worksheet("guests")

        # gspread columns are 1-indexed. Update STATUS in col 3, GUEST_COUNT in col 4.
        sheet.update_cell(row_index, 3, status)
        sheet.update_cell(row_index, 4, str(guest_count))

        # Update session state to reflect the change immediately
        st.session_state.guest_info['status'] = status
        st.session_state.guest_info['guest_count'] = guest_count
        return True
    except Exception as e:
        st.error(f"Произошла ошибка при обновлении: {e}")
        return False

# --- RSVP Form ---
st.header(t["rsvp_intro"])

guest_info = st.session_state.guest_info

# Check if the guest has already responded
if guest_info and guest_info['status'] in ['Yes', 'No']:
    st.success(t["thank_you"])
else:
    # Personalize the question for the logged-in guest
    rsvp_question = f"{guest_info['name']}, {t['rsvp_question'][0].lower()}{t['rsvp_question'][1:]}"

    with st.form(key="rsvp_form"):
        attendance = st.radio(
            label=rsvp_question,
            options=[t['rsvp_yes_1'], t['rsvp_yes_2'], t['rsvp_no']],
            index=None,
            key="attendance_radio")
        submitted = st.form_submit_button(label=t["submit_button"])
        if submitted:
            if attendance is not None:
                new_status = ""
                new_guest_count = 0
                if attendance == t['rsvp_yes_1']:
                    new_status = "Yes"
                    new_guest_count = 1
                elif attendance == t['rsvp_yes_2']:
                    new_status = "Yes"
                    new_guest_count = 2
                elif attendance == t['rsvp_no']:
                    new_status = "No"
                    new_guest_count = 0

                if update_rsvp(guest_info['row_index'], new_status, new_guest_count):
                    st.rerun()
                else:
                    st.warning("Пожалуйста, выберите один из вариантов / Опциялардың бірін таңдаңыз")



st.write("")

st.markdown(f""" <div class='glow-block'>
    <h3>{t['countdown_text']}</h3>
    <h3>{get_countdown(wedding_date, t)}</h3>
    <h3>{t['countdown_2']}</h3>
</div> """, unsafe_allow_html=True)

st.markdown(f""" <div class='glow-block'>
    <h3>{t['final_message']}
    <h3>{t['farewell']}</h3>
    <h2> <span style="color:white"> {t['farewell_names']} </span> </h2>
</div> """, unsafe_allow_html=True)
