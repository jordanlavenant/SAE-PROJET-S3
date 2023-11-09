document.getElementById('btn-pdf').addEventListener('click', function() {
    let lienTelechargement = document.createElement('a');
    lienTelechargement.href = './test.pdf'; // Remplacez cela par le chemin de votre fichier

    // Définissez l'attribut download pour spécifier le nom du fichier lors du téléchargement
    lienTelechargement.download = 'test.pdf';

    // Ajoutez le lien à la page
    document.body.appendChild(lienTelechargement);

    // Simulez un clic sur le lien pour déclencher le téléchargement
    lienTelechargement.click();

    // Supprimez le lien de la page une fois le téléchargement terminé
    document.body.removeChild(lienTelechargement);
});
 