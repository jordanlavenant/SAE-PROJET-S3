const boutonHautPage = document.querySelector('.fleche_haut_button');

boutonHautPage.addEventListener("click", () => {
    window.scroll({
        top: 0,
        behavior: "smooth"
    });
});

// Ajoutez un gestionnaire d'événement pour le défilement de la page
window.addEventListener("scroll", function () {
    // Vérifiez si la position de défilement est supérieure à 100 pixels
    if (window.scrollY > 100) {
        // Affichez le bouton
        boutonHautPage.style.display = "block";
    } else {
        // Masquez le bouton
        boutonHautPage.style.display = "none";
    }
});

let docTitle = document.title;
window.addEventListener("blur", function () {
    document.title = "Come back 🙄";
});

window.addEventListener("focus", function () {
    document.title = docTitle;
});