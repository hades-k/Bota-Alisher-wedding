document.addEventListener('DOMContentLoaded', function() {
    const ruBtn = document.getElementById('lang-ru');
    const kzBtn = document.getElementById('lang-kz');

    const ruElements = document.querySelectorAll('.ru');
    const kzElements = document.querySelectorAll('.kz');

    function setLanguage(lang) {
        if (lang === 'ru') {
            ruElements.forEach(el => el.style.display = 'block');
            kzElements.forEach(el => el.style.display = 'none');
            ruBtn.classList.add('active');
            kzBtn.classList.remove('active');
        } else {
            ruElements.forEach(el => el.style.display = 'none');
            kzElements.forEach(el => el.style.display = 'block');
            kzBtn.classList.add('active');
            ruBtn.classList.remove('active');
        }
    }

    ruBtn.addEventListener('click', () => setLanguage('ru'));
    kzBtn.addEventListener('click', () => setLanguage('kz'));

    // Set initial language
    setLanguage('ru');
});