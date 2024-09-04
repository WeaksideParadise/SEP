// script.js
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

function open_inspect_modal(ressource_id) {

    document.getElementById("resourceModal").style.display = "block";
    document.querySelector(".navigation-buttons").style.display = "none"; // Pfeile ausblenden

    // Fetch-API zum Senden der Anfrage an die Flask-Route
    fetch('/inspect_ressource', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ressource_id: ressource_id })  // Integer-Wert als JSON übergeben
    })  
        .then(response => response.json())  // Antwort in JSON umwandeln
        
        .then(data => {
            // Ergebnis in eine lesbare Form umwandeln
            document.getElementById('link').value = data.ressource_link;
            document.getElementById('description').value = data.ressource_description;
            document.getElementById('name').value = data.ressource_name;
            document.getElementById('opening_hours').value = data.ressource_opening_hours;
            document.getElementById('faculty').value = data.ressource_faculty;
            document.getElementById('ressource_type').value = data.ressource_type;
            document.getElementById("created_by").value = data.ressource_created_by;

            document.getElementById("resourceModal").style.display = "block";
            document.querySelector(".navigation-buttons").style.display = "none"; // Pfeile ausblenden
        })

        .catch((error) => {
            console.error('Fehler:', error);
        });
}

function close_inspect_modal() {
    document.getElementById("resourceModal").style.display = "none";
    document.querySelector(".navigation-buttons").style.display = "flex"; // Pfeile wieder anzeigen
}

function openAddResourceModal() {
    document.getElementById("addResourceModal").style.display = "block";
    document.querySelector(".navigation-buttons").style.display = "none"; // Pfeile ausblenden
}

function closeAddResourceModal() {
    document.getElementById("addResourceModal").style.display = "none";
    document.querySelector(".navigation-buttons").style.display = "flex"; // Pfeile wieder anzeigen
}

// Funktion zum Erhöhen der Likes
function increaseLikes() {
    var likeCount = document.getElementById("likeCount");
    var currentLikes = parseInt(likeCount.innerText);
    likeCount.innerText = currentLikes + 1;
}