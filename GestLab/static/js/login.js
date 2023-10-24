document.addEventListener("DOMContentLoaded", function() {
    let estAfficher = false;
    const btnChangerMDP = document.getElementById("btn-changer-mdp");
    const lienDeco = document.getElementById("seDeco");
    const lienAccueil = document.getElementById("lien-accueil");
    const formChangerMDP = document.getElementById("changerMDP-container");

    
    // Définir la fonction pour masquer l'élément
    function masquerElement() {
        if(!estAfficher) {
        lienDeco.style.display = "none";
        lienAccueil.style.display = "none";
        formChangerMDP.style.display = "flex";
        } else {
        lienDeco.style.display = "block";
        lienAccueil.style.display = "block";
        formChangerMDP.style.display = "none";
        }
        estAfficher = !estAfficher;
    }

    // Ajouter un écouteur d'événement sur le bouton pour appeler la fonction masquerElement lors du clic
    btnChangerMDP.addEventListener("click", masquerElement);
});
