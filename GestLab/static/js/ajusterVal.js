document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('.section-contenu');

    sections.forEach(function(section) {
        const boutonMoins = section.querySelector('.bouton-moins');
        const boutonPlus = section.querySelector('.bouton-plus');
        const valeurParagraphe = section.querySelector('.nb-choisit');
        let valeur = 0;

        boutonMoins.addEventListener('click', function() {
            if (valeur > 0) {
                valeur--;
                valeurParagraphe.textContent = valeur;
            }
        });

        boutonPlus.addEventListener('click', function() {
            valeur++;
            valeurParagraphe.textContent = valeur;
        });
    });
});
