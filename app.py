import streamlit as st
import pandas as pd
import os
import base64

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
    background_image_path = "background.png"
    encoded_image = get_base64_of_bin_file(background_image_path)
    if encoded_image:
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
    /* Main container styling */
    .main .block-container {{
        background-color: rgba(0, 0, 0, 0.8);
        border: 2px solid #feda4a;
        box-shadow: 0 0 20px #feda4a;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
    }}
    h1, h2, h3, p, label, .st-emotion-cache-16txtl3 {{
        font-family: 'Orbitron', sans-serif;
        color: #feda4a;
    }}
    h1 {{ text-transform: uppercase; }}
    h2 {{ color: #fff; }}
    .stButton>button {{
        border: 2px solid #feda4a;
        background-color: #feda4a;
        color: #000;
        padding: 10px 24px;
        border-radius: 5px;
        font-weight: bold;
        text-transform: uppercase;
        width: 100%;
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
        "address_intro": "Наша сага продолжится по адресу:",
        "address_placeholder": "[Укажите здесь адрес]",
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
        "address_intro": "Біздің дастанымыз мына мекен-жайда жалғасады:",
        "address_placeholder": "[Мекен-жайды осында көрсетіңіз]",
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

# --- Main App Logic ---
load_css()

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

# --- RSVP Form ---
st.header(t["rsvp_intro"])

# Use session state to check if the form has already been submitted
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# If form has been submitted, show thank you message. Otherwise, show the form.
if st.session_state.form_submitted:
    st.success(t["thank_you"])
else:
    with st.form(key="rsvp_form"):
        guest_name = st.text_input(label=t["form_name"])
        attendance = st.radio(
            label=t["form_attendance"],
            options=[t["option_yes"], t["option_no"]]
        )
        submitted = st.form_submit_button(label=t["submit_button"])

        if submitted:
            if not guest_name.strip():
                st.error(t["error_name"])
            else:
                # Record the submission
                response_data = pd.DataFrame([{
                    "Name": guest_name.strip(),
                    "Attendance": attendance,
                    "Timestamp": datetime.datetime.now()
                }])
                
                # Save to CSV
                if not os.path.exists(RSVP_FILE):
                    response_data.to_csv(RSVP_FILE, index=False, header=True)
                else:
                    response_data.to_csv(RSVP_FILE, mode='a', header=False, index=False)
                
                # Set state to show thank you message on rerun
                st.session_state.form_submitted = True
                st.rerun()