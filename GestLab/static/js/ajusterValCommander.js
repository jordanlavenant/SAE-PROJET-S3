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
                url: '/commander-materiel-unique/'+idUser+'?idMat='+idMat+'&qte='+maVariableJavaScript,
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
                console.log(maVariableJavaScript);
            }
            if (valeur == 0) {
                // Appliquer les règles CSS
                boutonAjout.style.pointerEvents = "none";
                boutonAjout.style.cursor = "not-allowed";
                boutonAjout.style.opacity = "0.5";
            }
            $.ajax({
                url: '/commander-materiel-unique/'+idUser+'?idMat='+idMat+'&qte='+maVariableJavaScript,
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
            if (valeur == 0) {
                // Appliquer les règles CSS
                boutonAjout.style.pointerEvents = "none";
                boutonAjout.style.cursor = "not-allowed";
                boutonAjout.style.opacity = "0.5";
            }
            $.ajax({
                url: '/commander-materiel-unique/'+idUser+'?idMat='+idMat+'&qte='+maVariableJavaScript,
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

    let sousContainerPaginations = document.querySelectorAll('.sous-container-pagination');

    sousContainerPaginations.forEach(function(sousContainerPagination) {
        let lienRechercheDemande = sousContainerPagination.querySelector('.lien-recherche-demande');
        let searchValue = document.querySelector('#search-bar').value;
        lienRechercheDemande.addEventListener('click', function() {
            console.log(searchValue);
            window.location.href = '/recherche-materiel?page='+lienRechercheDemande.textContent+'&value=' + searchValue;
        });
    });
});
