document.addEventListener('DOMContentLoaded', function() {
    let lienRechercheDemandes = document.querySelectorAll('.lien-recherche-demande');
    let searchValue = document.querySelector('#search-bar').value;

    for (let i = 0; i < lienRechercheDemandes.length; i++) {
        lienRechercheDemandes[i].addEventListener('click', function() {
            window.location.href = '/rechercher-inventaire?page='+lienRechercheDemandes[i].textContent+'&value=' + searchValue;
        });
    }
});
