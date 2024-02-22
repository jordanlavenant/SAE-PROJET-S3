const boutonHautPage = document.querySelector('.fleche_haut_button');
const header = document.querySelector('.header');
const title = document.querySelector('.title');
const nav = document.querySelector('.nav');
const navListe = document.querySelector('.nav-liste-elem');
const imgLogo = document.querySelector('.icon-logo-gestlab');
const imgCompte = document.querySelector('.img-compte');
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
        imgCompte.style.height = "50px";
        filAriane.style.transform = "translateY(-55px)";
        filAriane.style.paddingLeft = "50px";
        let pages = filAriane.querySelectorAll('a');
        pages.forEach(page => {
            page.style.color = "white";
        });
        let svgs = filAriane.querySelectorAll('svg');
        svgs.forEach(svg => {
            svg.style.fill = "white";
        });
    } else {
        title.style.paddingTop = "0";
        divSousHeader.style.top = "0";
        divSousHeader.style.position = "relative";
        nav.style.position = "relative";
        boutonHautPage.style.display = "none";
        nav.style.padding = "20px 0";
        navListe.style.m = "0 20px";
        imgLogo.style.height = "100px";
        imgCompte.style.height = "100px";
        filAriane.style.transform = "translateY(0)";
        filAriane.style.paddingLeft = "0";
        let pages = filAriane.querySelectorAll('a');
        pages.forEach(page => {
            page.style.color = "#009AF0";
        });
        let svgs = filAriane.querySelectorAll('svg');
        svgs.forEach(svg => {
            svg.style.fill = "#009AF0";
        });
    }
});