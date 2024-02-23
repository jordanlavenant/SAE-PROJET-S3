document.addEventListener("DOMContentLoaded", function() {
    const formLogin = document.getElementById("login-container");
    const formMdpOublier = document.getElementById("mdp-container");
    const boutonMdpOublier = document.getElementById("btn-mdp-oublier");
    const boutonRetourMdp = document.getElementById("btn-retour-mdp");

    /**
     * Masque le formulaire de connexion et affiche le formulaire de récupération de mot de passe.
     */
    function masquerLogin() {
        console.log("test");
        formLogin.style.display = "none";
        formMdpOublier.style.display = "flex";
    }

    /**
     * Fonction qui affiche le formulaire de connexion et masque le formulaire de récupération de mot de passe.
     */
    function retour(){
        formLogin.style.display = "flex";
        formMdpOublier.style.display = "none";
    }

    // Ajouter un écouteur d'événement sur le bouton pour appeler la fonction masquerElement lors du clic
    boutonMdpOublier.addEventListener("click", masquerLogin);
    boutonRetourMdp.addEventListener("click", retour);
});
