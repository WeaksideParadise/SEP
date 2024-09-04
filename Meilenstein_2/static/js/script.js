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
        body: JSON.stringify({ ressource_id: parseInt(ressource_id) })  // Integer-Wert als JSON übergeben
    })  
        .then(response => response.json())  // Antwort in JSON umwandeln
        
        .then(data => {
            // Ergebnis in eine lesbare Form umwandeln
            document.getElementById("i_ressource_id").value = ressource_id
            document.getElementById("i_link").value = data.ressource_link;
            document.getElementById("i_description").value = data.ressource_description;
            document.getElementById("i_name").value = data.ressource_name;
            document.getElementById("i_opening_hours").value = data.ressource_opening_hours;
            document.getElementById("i_faculty").value = data.ressource_faculty;
            document.getElementById("i_ressource_type").value = data.ressource_type;
            document.getElementById("i_created_by").value = data.ressource_created_by;
            document.getElementById("i_like_count").value = data.ressource_likes

            if (data.ressource_is_liked) {
                document.getElementById("i_like_count").querySelector(".icon").innerHTML = '&#10084';
            } else {
                document.getElementById("i_like_count").querySelector(".icon").innerHTML = '&#9829';
                document.getElementById("i_like_count").style.color = '#000000'
            }

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
function like_ressource() {
    ressource_id = parseInt(document.getElementById("i_ressource_id").value)

    fetch('/like_ressource', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ressource_id: ressource_id })  // Integer-Wert als JSON übergeben
    })  
        .then(response => response.json())  // Antwort in JSON umwandeln
        
        .then(data => {
            if (data.status) {
                if (document.getElementById("i_like_count").querySelector(".icon").innerHTML == '&#10084'){
                    document.getElementById("i_like_count").querySelector(".icon").innerHTML = '&#9829';
                    document.getElementById("i_like_count").style.color = '#000000';
                    document.getElementById("i_like_count").value -= 1;
                }
                else {
                    document.getElementById("i_like_count").querySelector(".icon").innerHTML = '&#10084';
                    document.getElementById("i_like_count").value -= 1;
                }
            } else {
                console.error('Liken fehlgeschlagen');
            }
        })

        .catch((error) => {
            console.error('Fehler:', error);
        });
}