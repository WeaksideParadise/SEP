function open_inspect_modal(ressource_id, elementIds) {

    document.getElementById("resourceModal").style.display = "block";

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
            document.getElementById(elementIds.ressource_id).value  = ressource_id
            document.getElementById(elementIds.link).value          = data.ressource_link;
            document.getElementById(elementIds.description).value   = data.ressource_description;
            document.getElementById(elementIds.name).value          = data.ressource_name;
            document.getElementById(elementIds.hours).value         = data.ressource_opening_hours;
            document.getElementById(elementIds.faculty).value       = data.ressource_faculty;
            document.getElementById(elementIds.ressource_type).value= data.ressource_type;
            document.getElementById(elementIds.created_by).value    = data.ressource_created_by;
            document.getElementById(elementIds.like_count).innerHTML= data.ressource_likes;

            // Like basierte Anzeige
            if (data.ressource_is_liked) {
                document.getElementById(elementIds.like_emoji).innerHTML = '&#10084';
            } else {
                document.getElementById(elementIds.like_emoji).innerHTML = '&#10084';
                //document.getElementById(elementIds.like_emoji).style.color = '#000000';
            }

            // Rechte basierte Anzeige
            if(data.has_rights){
                if(data.ressource_is_published){
                    document.getElementById(elementIds.is_published).value  = 'ist veröffentlicht';
                }
                else{
                    document.getElementById(elementIds.is_published).value  = 'ist nicht veröffentlicht';
                    document.getElementById(elementIds.is_published).style.backgroundColor = 'red';
                }
                // document.getElementById(elementIds.is_published).visibility  = ....
            }
        })

        .catch((error) => {
            console.error('Fehler:', error);
        });
}

function close_inspect_modal() {
    document.getElementById("resourceModal").style.display = "none";
}

function like_ressource() {
    let ressource_id = parseInt(document.getElementById("i_ressource_id").value)

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

function report_ressource(elementIds) {

    let ressource_id = document.getElementById(elementIds.ressource_id).value;
    let reason = document.getElementById(elementIds.reason).value;

    // Fetch-API zum Senden der Anfrage an die Flask-Route
    fetch('/report_ressource', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ressource_id: parseInt(ressource_id), reason: reason })  // Integer-Wert als JSON übergeben
    })  
    
    .then(response => response.json())  // Antwort in JSON umwandeln
        
    .then(data => {
        if (data.status) {
            document.getElementById(elementIds.reason).value = "";
        } 
    })

    .catch((error) => {
        console.error('Fehler:', error);
    });
}