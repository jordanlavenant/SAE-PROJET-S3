document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('.section-contenu');

    sections.forEach(function(section) {
        const boutonMoins = section.querySelector('.bouton-moins');
        const boutonPlus = section.querySelector('.bouton-plus');
        const valeurParagraphe = section.querySelector('.nb-choisit');
        const boutonAjout = section.querySelector(".ajouter-demande");
        const liens = section.querySelector("#ajouter-demande-content");
        const ref = section.querySelector(".ref");
        let classes = liens.classList;
        let idMat = classes[0];
        let valeur = classes[1];
        console.log(maVariableJavaScript);

        boutonAjout.addEventListener("click", function() {
            url = `/demander-materiel-unique/${idUser}?idMat=${idMat}&qte=${maVariableJavaScript}`;
            window.location.href = url;
        });

        boutonMoins.addEventListener('click', function() {
            if (valeur > 0) {
                // Appliquer les règles CSS
                boutonAjout.style.pointerEvents = "all";
                boutonAjout.style.cursor = "pointer";
                boutonAjout.style.opacity = "1";
                valeur--;
                valeurParagraphe.textContent = valeur;
                maVariableJavaScript = valeur;
                ref.style.color = "white";
                console.log(maVariableJavaScript);
            }
            if (valeur == 0) {
                // Appliquer les règles CSS
                boutonAjout.style.pointerEvents = "none";
                boutonAjout.style.cursor = "not-allowed";
                boutonAjout.style.opacity = "0.5";
                ref.style.color = "rgb(164,164,164)";
            }
        });

        boutonPlus.addEventListener('click', function() {
            // Appliquer les règles CSS
            boutonAjout.style.pointerEvents = "all";
            boutonAjout.style.cursor = "pointer";
            boutonAjout.style.opacity = "1";
            valeur++;
            valeurParagraphe.textContent = valeur;
            maVariableJavaScript = valeur;
            console.log(maVariableJavaScript);
            ref.style.color = "white";
            if (valeur == 0) {
                // Appliquer les règles CSS
                boutonAjout.style.pointerEvents = "none";
                boutonAjout.style.cursor = "not-allowed";
                boutonAjout.style.opacity = "0.5";
                ref.style.color = "rgb(164,164,164)";
            }
        });
    });
});
