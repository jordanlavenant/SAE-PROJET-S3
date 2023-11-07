document.addEventListener("DOMContentLoaded", function() {
    let estAfficher = false;
    let estAfficherMail = false;
    let estAfficherMDP = false;
    const btnChangerMDP = document.getElementById("btn-changer-mdp");
    const btnChangerMail = document.getElementById("btn-changer-mail");
    const btnRetour = document.getElementById("btn-retour");
    const lienDeco = document.getElementById("seDeco");
    const lienAccueil = document.getElementById("lien-accueil");
    const formChangerMDP = document.getElementById("ChangerMDPForm");
    const formChangerMail = document.getElementById("ChangerMailForm");
    const formLogin = document.getElementById("login-container");
    const formMdpOublier = document.getElementById("mdp-container");
    const boutonMdpOublier = document.getElementById("btn-mdp-oublier");
    const boutonTest = document.querySelector("btn-mdp-oublier")

    
    // Définir la fonction pour masquer l'élément
    function masquerMDP() {
        if(!estAfficher) {
            lienDeco.style.display = "none";
            lienAccueil.style.display = "none";
            btnChangerMDP.style.display = "none";
            btnChangerMail.style.display = "none";
            btnRetour.style.display = "block";
            formChangerMDP.style.display = "flex";
            estAfficher = true;
        }
    }

    // Définir la fonction pour masquer l'élément
    function masquerMail() {
            if(!estAfficher) {
                lienDeco.style.display = "none";
                lienAccueil.style.display = "none";
                btnChangerMDP.style.display = "none";
                btnChangerMail.style.display = "none";
                btnRetour.style.display = "block";
                formChangerMail.style.display = "flex";
                estAfficher = true;
            } 
    }

    // Définir la fonction pour masquer l'élément
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

    function masquerLogin() {
        console.log("test");
        // formLogin.style.display = "none";
        // formMdpOublier.style.display = "flex";
    }

    // Ajouter un écouteur d'événement sur le bouton pour appeler la fonction masquerElement lors du clic
    btnChangerMDP.addEventListener("click", masquerMDP);
    btnChangerMail.addEventListener("click", masquerMail);
    btnRetour.addEventListener("click", masquerTout);
    boutonMdpOublier.addEventListener("click", masquerLogin);
    boutonTest.addEventListener("click", masquerLogin);
});
