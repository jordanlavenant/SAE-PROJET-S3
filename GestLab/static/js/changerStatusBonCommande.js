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