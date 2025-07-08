document.addEventListener('DOMContentLoaded', function() {
    const yesBtn = document.getElementById('yes-btn');
    const noBtn = document.getElementById('no-btn');
    const confirmation = document.getElementById('confirmation');

    yesBtn.addEventListener('click', function() {
        confirmation.classList.remove('hidden');
        yesBtn.style.display = 'none';
        noBtn.style.display = 'none';
    });

    noBtn.addEventListener('click', function() {
        confirmation.classList.remove('hidden');
        yesBtn.style.display = 'none';
        noBtn.style.display = 'none';
    });
});