const boutonHautPage = document.querySelector('.fleche_haut_button');
const header = document.querySelector('.header');
const title = document.querySelector('.title');
const nav = document.querySelector('.nav');
const navListe = document.querySelector('.nav-liste-elem');
const imgLogo = document.querySelector('.icon-logo-gestlab');
const divSousHeader = document.querySelector('.sous-header');
const filAriane = document.querySelector('#fil-ariane');

boutonHautPage.addEventListener("click", () => {
    window.scroll({
        top: 0,
        behavior: "smooth"
    });
});

// Ajoutez un gestionnaire d'événement pour le défilement de la page
window.addEventListener("scroll", function () {
    // Vérifiez si la position de défilement est supérieure à 100 pixels
    if (window.scrollY > 10) {
        title.style.paddingTop = "2em";
        nav.style.position = "fixed"; 
        nav.style.width = "100%";
        divSousHeader.style.top = "2em";
        divSousHeader.style.position = "fixed";
        divSousHeader.style.width = "98vw";
        boutonHautPage.style.display = "block";
        nav.style.padding = "0";
        navListe.style.margin = "0";
        imgLogo.style.height = "50px";
        filAriane.style.transform = "translateY(-60px)";
        filAriane.style.paddingLeft = "50px";
    } else {
        title.style.paddingTop = "0";
        divSousHeader.style.top = "0";
        divSousHeader.style.position = "relative";
        nav.style.position = "relative";
        boutonHautPage.style.display = "none";
        nav.style.padding = "20px 0";
        navListe.style.m = "0 20px";
        imgLogo.style.height = "100px";
        // divSousHeader.style.backgroundColor = "transparent";
        filAriane.style.transform = "translateY(0)";
        filAriane.style.paddingLeft = "0";
    }
});

let docTitle = document.title;
window.addEventListener("blur", function () {
    document.title = "Come back 🙄";
});

window.addEventListener("focus", function () {
    document.title = docTitle;
});