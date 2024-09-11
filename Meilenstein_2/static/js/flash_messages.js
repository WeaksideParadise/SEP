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


function flashMessage(message, type) {

    const ids = ["index_flash_js", "search_flash_js", "admin_flash_js", "admin2_flash_js"];
    let flash_element = null;
    let flash_element_type = null;

    for (const id of ids) {
        flash_element = document.getElementById(id);
        flash_element_type = document.getElementById(id + "_type")
        if (flash_element) break;
    }

    if (flash_element) {
        flash_element_type.querySelectorAll('.flash').forEach(flash => {
            flash.classList.remove('success', 'error');
        });

        let flashClass = '';
        if (type == "success") {
            flashClass = 'success';

        } else {
            flashClass = 'error';
        }

        flash_element_type.classList.add(flashClass);

        flash_element.querySelector('.flash').innerHTML = `${message}<span class="close-btn">&times;</span>`;

        flash_element.style.display = "block";

        const closeButtons = document.querySelectorAll('.close-btn');

        closeButtons.forEach(button => {
            button.addEventListener('click', (event) => {
                const flashMessage = event.target.closest('.flash');
                if (flashMessage) {
                    flashMessage.style.display = 'none';
                }
            });
        });
    }

}