import streamlit as st
import pandas as pd
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Бота & Алишер",
    page_icon="💍",
    layout="wide"
)

# --- File for RSVPs ---
RSVP_FILE = "rsvps.csv"

# --- Load Custom CSS for Star Wars Theme ---
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    /* General Styles */
    body {
        background-color: #000;
        color: #feda4a; /* Star Wars Gold */
    }
    .stApp {
        background-image: url("https://www.nasa.gov/wp-content/uploads/2023/11/hubble-ngc346-potw.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stApp > header { 
        background-color: transparent; 
    }
    .main .block-container {
        background-color: rgba(0, 0, 0, 0.75);
        border: 2px solid #feda4a;
        box-shadow: 0 0 20px #feda4a;
        padding: 2rem;
        border-radius: 10px;
        max-width: 700px;
        margin: auto;
    }
    h1, h2, h3, p, label {
        font-family: 'Orbitron', sans-serif;
        color: #feda4a;
    }
    h1 { text-transform: uppercase; }
    h2 { color: #fff; }
    .stButton>button {
        border: 2px solid #feda4a;
        background-color: #feda4a;
        color: #000;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background-color: #000;
        color: #feda4a;
    }
    .intro-text {
        font-size: 1.2em;
        line-height: 1.6;
        text-align: center;
        transform: perspective(300px) rotateX(15deg);
        margin-bottom: 2em;
    }
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
        "address_intro": "Наша сага продолжится по адресу:",
        "address_placeholder": "[Укажите здесь адрес]",
        "rsvp_intro": "Да пребудет с вами Сила! Подтвердите свое присутствие до 20.08.2025",
        "form_name": "Ваше имя (Имена гостей)",
        "form_attendance": "Подтверждаете присутствие?",
        "option_yes": "Да, я присоединюсь к Альянсу",
        "option_no": "Нет, я на стороне Империи",
        "submit_button": "Отправить ответ",
        "thank_you": "Спасибо! Ваш ответ записан в голокрон.",
        "error_name": "Пожалуйста, введите ваше имя, юный падаван.",
        "admin_toggle": "Показать список гостей",
        "guest_list_header": "Список гостей Альянса"
    },
    "kz": {
        "title": "Ботагоз & Әлішер",
        "intro": "Ерте, ерте заманда, алыс-алыс галактикада...",
        "header": "Үйлену тойына шақыру",
        "alliance": "Сіздерді біздің одағымыздың құрылу салтанатына шақырамыз!",
        "date": "06.09.2025",
        "address_intro": "Біздің дастанымыз мына мекен-жайда жалғасады:",
        "address_placeholder": "[Мекен-жайды осында көрсетіңіз]",
        "rsvp_intro": "Күш сізбен бірге болсын! Қатысуыңызды 20.08.2025 дейін растаңыз",
        "form_name": "Сіздің есіміңіз (Қонақтардың есімдері)",
        "form_attendance": "Қатысуды растайсыз ба?",
        "option_yes": "Иә, мен Альянсқа қосыламын",
        "option_no": "Жоқ, мен Империя жағындамын",
        "submit_button": "Жауапты жіберу",
        "thank_you": "Рахмет! Сіздің жауабыңыз голокронға жазылды.",
        "error_name": "Есіміңізді енгізіңіз, жас падаван.",
        "admin_toggle": "Қонақтар тізімін көрсету",
        "guest_list_header": "Альянс қонақтарының тізімі"
    }
}

# --- Main App ---
load_css()

# Language Selection
lang_choice = st.sidebar.radio("Language / Тіл", ["Русский", "Қазақ"], label_visibility="collapsed")
lang = "ru" if lang_choice == "Русский" else "kz"

# Get translated content
t = content[lang]

st.title(t["title"])
st.header(t["header"])

st.markdown(f'<p class="intro-text">{t["intro"]}</p>', unsafe_allow_html=True)

st.write(t["alliance"])
st.subheader(t["date"])

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
            # Save the response
            new_data = pd.DataFrame([[guest_name, attendance]])
            if not os.path.exists(RSVP_FILE):
                new_data.to_csv(RSVP_FILE, index=False, header=["Name", "Attendance"])
            else:
                new_data.to_csv(RSVP_FILE, mode='a', header=False, index=False)
            
            st.success(t["thank_you"])

# --- Admin Section to View RSVPs ---
st.markdown("---")
if st.checkbox(t["admin_toggle"]):
    st.header(t["guest_list_header"])
    if os.path.exists(RSVP_FILE):
        df = pd.read_csv(RSVP_FILE)
        st.dataframe(df)
    else:
        st.warning("Голокрон пока пуст. / Голокрон әлі бос.")
