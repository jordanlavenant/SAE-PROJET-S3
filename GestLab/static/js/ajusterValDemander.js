/**
 * Ce code est responsable de la gestion de l'ajustement des valeurs dans un formulaire.
 * Il écoute l'événement 'DOMContentLoaded' et effectue différentes actions en fonction des interactions de l'utilisateur.
 * Le code utilise AJAX pour envoyer des requêtes au serveur et mettre à jour l'interface utilisateur en conséquence.
 * Il inclut également des écouteurs d'événements pour les clics sur les boutons et les changements de saisie.
 * @file Ce fichier est situé à /C:/Users/loulo/Desktop/guthub/SAE-PROJET-S3/GestLab/static/js/ajusterValDemander.js
 */
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

        valeurParagraphe.addEventListener('change', function() {
            boutonMoins.style.pointerEvents = "none";
            boutonMoins.style.cursor = "not-allowed";
            boutonMoins.style.opacity = "0.5";

            boutonPlus.style.pointerEvents = "none";
            boutonPlus.style.cursor = "not-allowed";
            boutonPlus.style.opacity = "0.5";
            if (valeur > 0) {
                // Appliquer les règles CSS
                boutonAjout.style.pointerEvents = "all";
                boutonAjout.style.cursor = "pointer";
                boutonAjout.style.opacity = "1";
                valeur = valeurParagraphe.value;
                // valeurParagraphe.value = valeur;
                maVariableJavaScript = valeur;
                console.log(maVariableJavaScript);
            }
            if (valeur == 0) {
                // Appliquer les règles CSS
                boutonAjout.style.pointerEvents = "none";
                boutonAjout.style.cursor = "not-allowed";
                boutonAjout.style.opacity = "0.5";
            }
            $.ajax({
                url: '/demander-materiel-unique/'+idUser+'?idMat='+idMat+'&qte='+maVariableJavaScript,
                type: 'GET',
                success: function(response) {
                    console.log(response);
                    boutonMoins.style.pointerEvents = "all";
                    boutonMoins.style.cursor = "pointer";
                    boutonMoins.style.opacity = "1";

                    boutonPlus.style.pointerEvents = "all";
                    boutonPlus.style.cursor = "pointer";
                    boutonPlus.style.opacity = "1";
                }
            });
        });

        boutonMoins.addEventListener('click', function() {
            boutonMoins.style.pointerEvents = "none";
            boutonMoins.style.cursor = "not-allowed";
            boutonMoins.style.opacity = "0.5";

            boutonPlus.style.pointerEvents = "none";
            boutonPlus.style.cursor = "not-allowed";
            boutonPlus.style.opacity = "0.5";
            if (valeur > 0) {
                // Appliquer les règles CSS
                boutonAjout.style.pointerEvents = "all";
                boutonAjout.style.cursor = "pointer";
                boutonAjout.style.opacity = "1";
                valeur--;
                valeurParagraphe.value = valeur;
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
            $.ajax({
                url: '/demander-materiel-unique/'+idUser+'?idMat='+idMat+'&qte='+maVariableJavaScript,
                type: 'GET',
                success: function(response) {
                    console.log(response);
                    boutonMoins.style.pointerEvents = "all";
                    boutonMoins.style.cursor = "pointer";
                    boutonMoins.style.opacity = "1";

                    boutonPlus.style.pointerEvents = "all";
                    boutonPlus.style.cursor = "pointer";
                    boutonPlus.style.opacity = "1";
                }
            });
        });

        boutonPlus.addEventListener('click', function() {
            // Appliquer les règles CSS
            boutonMoins.style.pointerEvents = "none";
            boutonMoins.style.cursor = "not-allowed";
            boutonMoins.style.opacity = "0.5";

            boutonPlus.style.pointerEvents = "none";
            boutonPlus.style.cursor = "not-allowed";
            boutonPlus.style.opacity = "0.5";
            valeur++;
            valeurParagraphe.value = valeur;
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
            $.ajax({
                url: '/demander-materiel-unique/'+idUser+'?idMat='+idMat+'&qte='+maVariableJavaScript,
                type: 'GET',
                success: function(response) {
                    console.log(response);
                    boutonMoins.style.pointerEvents = "all";
                    boutonMoins.style.cursor = "pointer";
                    boutonMoins.style.opacity = "1";

                    boutonPlus.style.pointerEvents = "all";
                    boutonPlus.style.cursor = "pointer";
                    boutonPlus.style.opacity = "1";
                }
            });
        });
    });


    let lienRechercheDemandes = document.querySelectorAll('.lien-recherche-demande');
    let searchValue = document.querySelector('#search-bar').value;

    for (let i = 0; i < lienRechercheDemandes.length; i++) {
        lienRechercheDemandes[i].addEventListener('click', function() {
            window.location.href = '/recherche-materiel-demander?page='+lienRechercheDemandes[i].textContent+'&value=' + searchValue;
        });
    }
});
