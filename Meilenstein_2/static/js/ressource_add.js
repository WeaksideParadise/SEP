function openAddResourceModal() {
    document.getElementById("addResourceModal").style.display = "block";
    document.querySelector(".navigation-buttons").style.display = "none"; // Pfeile ausblenden
}

function closeAddResourceModal() {
    document.getElementById("addResourceModal").style.display = "none";
    document.querySelector(".navigation-buttons").style.display = "flex"; // Pfeile wieder anzeigen
}