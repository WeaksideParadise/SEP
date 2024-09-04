document.addEventListener('DOMContentLoaded', () => {
    const closeButtons = document.querySelectorAll('.close-btn');

    closeButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const flashMessage = event.target.closest('.flash');
            if (flashMessage) {
                flashMessage.style.display = 'none';
            }
        });
    });
});


