document.addEventListener("DOMContentLoaded", function() {
    let estAfficher = false;
    let estAfficherMail = false;
    let estAfficherMDP = false;
    const btnChangerMDP = document.getElementById("btn-changer-mdp");
    const btnChangerMail = document.getElementById("btn-changer-mail");
    const btnRetour = document.getElementById("btn-back");
    const lienDeco = document.getElementById("seDeco");
    const lienAccueil = document.getElementById("lien-accueil");
    const formChangerMDP = document.getElementById("ChangerMDPForm");
    const formChangerMail = document.getElementById("ChangerMailForm");


    
    // Définir la fonction pour masquer l'élément
    /**
     * Masque le formulaire de changement de mot de passe et les éléments associés.
     */
    function masquerMDP() {
        if(!estAfficher) {
            lienDeco.style.display = "none";
            lienAccueil.style.display = "none";
            btnChangerMDP.style.display = "none";
            btnChangerMail.style.display = "none";
            btnRetour.style.display = "inline";
            formChangerMDP.style.display = "flex";
            estAfficher = true;
        }
    }

    // Définir la fonction pour masquer l'élément
    /**
     * Masque certains éléments et affiche un formulaire pour changer l'e-mail.
     */
    function masquerMail() {
            if(!estAfficher) {
                lienDeco.style.display = "none";
                lienAccueil.style.display = "none";
                btnChangerMDP.style.display = "none";
                btnChangerMail.style.display = "none";
                btnRetour.style.display = "inline";
                formChangerMail.style.display = "flex";
                estAfficher = true;
            } 
    }

    // Définir la fonction pour masquer l'élément
    /**
     * Masque tous les éléments liés au changement de mot de passe et d'email,
     * et affiche les éléments liés à la déconnexion, à la page d'accueil, et aux boutons de changement de mot de passe et d'email.
     */
    function masquerTout() {
        formChangerMDP.style.display = "none";
        formChangerMail.style.display = "none";
        btnRetour.style.display = "none";
        lienDeco.style.display = "block";
        lienAccueil.style.display = "block";
        btnChangerMDP.style.display = "block";
        btnChangerMail.style.display = "block";
        estAfficher = false;
        estAfficherMail = false;
        estAfficherMDP = false;
    }

    // Ajouter un écouteur d'événement sur le bouton pour appeler la fonction masquerElement lors du clic
    btnChangerMDP.addEventListener("click", masquerMDP);
    btnChangerMail.addEventListener("click", masquerMail);
    btnRetour.addEventListener("click", masquerTout);
});
