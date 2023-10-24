document.addEventListener("DOMContentLoaded", function() {
    let estAfficher = false;
    let estAfficherMail = false;
    let estAfficherMDP = false;
    const btnChangerMDP = document.getElementById("btn-changer-mdp");
    const btnChangerMail = document.getElementById("btn-changer-mail");
    const lienDeco = document.getElementById("seDeco");
    const lienAccueil = document.getElementById("lien-accueil");
    const formChangerMDP = document.getElementById("ChangerMDPForm");
    const formChangerMail = document.getElementById("ChangerMailForm");

    
    // Définir la fonction pour masquer l'élément
    function masquerMDP() {
        if(estAfficherMail){
            formChangerMail.style.display = "none";
            formChangerMDP.style.display = "flex";
            estAfficherMail = false;
            estAfficherMDP = true;
        } else {
            if(!estAfficher) {
                lienDeco.style.display = "none";
                lienAccueil.style.display = "none";
                formChangerMDP.style.display = "flex";
                estAfficherMDP = true;
            } else {
                lienDeco.style.display = "block";
                lienAccueil.style.display = "block";
                formChangerMDP.style.display = "none";
                estAfficherMDP = false;
            }
            estAfficher = !estAfficher;
        }
    }

    // Définir la fonction pour masquer l'élément
    function masquerMail() {
        if(estAfficherMDP){
            formChangerMDP.style.display = "none";
            formChangerMail.style.display = "flex";
            estAfficherMDP = false;
            estAfficherMail = true;
        } else {
            if(!estAfficher) {
                lienDeco.style.display = "none";
                lienAccueil.style.display = "none";
                formChangerMail.style.display = "flex";
                estAfficherMail = true;
            } else {
                lienDeco.style.display = "block";
                lienAccueil.style.display = "block";
                formChangerMail.style.display = "none";
                estAfficherMail = false;
            }
            estAfficher = !estAfficher;
        }
    }

    // Ajouter un écouteur d'événement sur le bouton pour appeler la fonction masquerElement lors du clic
    btnChangerMDP.addEventListener("click", masquerMDP);
    btnChangerMail.addEventListener("click", masquerMail);
});
