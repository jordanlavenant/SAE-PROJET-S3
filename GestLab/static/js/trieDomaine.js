const form = document.getElementById('formulaire-trie-domaine');
const maCombo = document.getElementById('domaine-select');

maCombo.addEventListener('change', function () {
    select_option = maCombo.value;
    console.log(select_option);
    const idForm = document.getElementById('formulaire-trie-domaine');
    const nbUser = parseInt(idForm.className)

    let sectionUser = document.getElementsByClassName("section-contenu");

    for(let i=0; i<nbUser; i++){
        sectionUser[i].style.display = "flex";
    }

    for(let i=0; i<nbUser; i++){
        let id = sectionUser[i].id;
        if(select_option == "Appareillage" && id != 1){
            sectionUser[i].style.display = "none";
        }
        if(select_option == "Électricité" && id != 2){
            sectionUser[i].style.display = "none";
        }
        if(select_option == "Matériel de laboratoire" && id != 3){
            sectionUser[i].style.display = "none";
        }
        if(select_option == "Médias" && id != 4){
            sectionUser[i].style.display = "none";
        }
        if(select_option == "Produits chimiques" && id != 5){
            sectionUser[i].style.display = "none";
        }
        if(select_option == "Verrerie et associés" && id != 6){
            sectionUser[i].style.display = "none";
        }
    }

    // form.submit();
    // changer val comboBox
});