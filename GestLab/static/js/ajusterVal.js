document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('.section-contenu');

    sections.forEach(function(section) {
        const boutonMoins = section.querySelector('.bouton-moins');
        const boutonPlus = section.querySelector('.bouton-plus');
        const valeurParagraphe = section.querySelector('.nb-choisit');
        const boutonAjout = section.querySelector(".ajouter-commande");
        const liens = section.querySelector('a');
        let classes = liens.classList;
        let idMat = classes[0];
        let valeur = classes[1];; 
        console.log(maVariableJavaScript);

        boutonAjout.addEventListener("click", function() {
            url = `/ajouter-materiel-unique/${idUser}?idMat=${idMat}&qte=${maVariableJavaScript}`;
            window.location.href = url;
        });

        boutonMoins.addEventListener('click', function() {
            if (valeur > 0) {
                valeur--;
                valeurParagraphe.textContent = valeur;
                maVariableJavaScript = valeur;
                console.log(maVariableJavaScript);
            }
        });

        boutonPlus.addEventListener('click', function() {
            valeur++;
            valeurParagraphe.textContent = valeur;
            maVariableJavaScript = valeur;
            console.log(maVariableJavaScript);
        });
    });
});
