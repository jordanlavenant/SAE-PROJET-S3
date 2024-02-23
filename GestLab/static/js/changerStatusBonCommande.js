/**
 * Attache un écouteur d'événement au chargement du document pour gérer le changement de statut d'un bon de commande.
 */
document.addEventListener('DOMContentLoaded', function() {
    const divs = document.querySelectorAll('.info-bon');

    divs.forEach(function(div) {
        const selectElement = div.querySelector('.statut');
        let classes = selectElement.classList;
        const idbc = classes[1];

        selectElement.addEventListener('change', function() {
            var selectedValue = selectElement.value;
            console.log('Option sélectionnée :', selectedValue);
            window.location.href = `/changer-statut-bon-commande?idbc=${idbc}&statut=` + selectedValue;
        });
    });

});

/**
 * Supprime un bon de commande.
 * @param {number} idbc - L'identifiant du bon de commande à supprimer.
 */
function deleteBonCommande(idbc) {
    event.stopPropagation();
    console.log(idbc);
    document.location=`/delete-bon-commande/${idbc}`;
}