const form = document.getElementById('formulaire-comboBox');
const maCombo = document.getElementById('categorie-select');
maCombo.addEventListener('change', function () {
    select_option = maCombo.value;
    const idForm = document.getElementById('categorie-select');
    const nbUser = parseInt(idForm.className)

    let sectionUser = document.getElementsByClassName("sous-container-info-utilisateur");

    for(let i=0; i<nbUser; i++){
        sectionUser[i].style.display = "flex";
    }

    for(let i=0; i<nbUser; i++){
        let id = sectionUser[i].id;
        if(select_option == "Professeur" && id != 2){
            sectionUser[i].style.display = "none";
        }
        if(select_option == "Gestionnaire" && id != 4){
            sectionUser[i].style.display = "none";
        }
        if(select_option == "Laborantin" && id != 3){
            sectionUser[i].style.display = "none";
        }
    }

    // form.submit();
    // changer val comboBox
});