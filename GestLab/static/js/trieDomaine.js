const form = document.getElementById('formulaire-trie-domaine');
const maCombo = document.getElementById('domaine-select');

maCombo.addEventListener('change', function () {
    select_option = maCombo.value;
    console.log(select_option);
    const idForm = document.getElementById('formulaire-trie-domaine');
    const nbMateriel = parseInt(idForm.className)

    console.log(nbMateriel);

    let sectionUser = document.querySelectorAll(".section-contenu");
    console.log(sectionUser);

    sectionUser.forEach(function(section) {
        section.style.display = "flex";
    });

    sectionUser.forEach(function(section) {
        let id = section.id;
        if(select_option == "Appareillage" && id != 1){
            section.style.display = "none";
        }
        if(select_option == "Électricité" && id != 2){
            section.style.display = "none";
        }
        if(select_option == "Matériel de laboratoire" && id != 3){
            section.style.display = "none";
        }
        if(select_option == "Médias" && id != 4){
            console.log("Médias et id = "+id);
            section.style.display = "none";
        }
        if(select_option == "Produits chimiques" && id != 5){
            section.style.display = "none";
        }
        if(select_option == "Verrerie et associés" && id != 6){
            section.style.display = "none";
        }
    });
});