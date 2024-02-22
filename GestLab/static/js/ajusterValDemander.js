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

    const searchBar = document.getElementById('search-bar');
    const searchBtn = document.getElementById('btn-search');

    // Obtenez la chaîne de requête de l'URL
    var queryString = window.location.search;

    // Créez un objet URLSearchParams à partir de la chaîne de requête
    var params = new URLSearchParams(queryString);

    // Obtenez la valeur de la variable 'value'
    var valueSearch = params.get('value');
    searchBar.value = valueSearch;

    searchBtn.addEventListener('click', function() {
        $.ajax({
            url: '/recherche-materiel-demander?value=' + valueSearch,
            type: 'GET',
            success: function(response) {
                console.log(response);
                // window.location.reload();
            }
        });
    });
});
