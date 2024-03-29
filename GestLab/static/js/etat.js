const parent = document.getElementsByClassName("item-card")

id_array = []

for (let i = 0; i < parent.length; i++) {
    id_array.push(parseInt(parent[i].id));
}

for (id in id_array) {
    let item = document.getElementById(`${id_array[id]}`);
    let alert = document.getElementById(`alerts_count_${id_array[id]}`);
    if (alert == null) {
        item.style.borderLeft = "#2EDD94 solid 15px";
    } else {
        item.style.borderLeft = "#d35252 solid 15px";
    }
}

/**
 * Bascule la visibilité d'un élément popup et met à jour le style overflow de l'élément HTML en conséquence.
 */
function togglePopup() {
    document.querySelector('.popup').classList.toggle('open');
    html.style.overflow = html.style.overflow === 'hidden' ? 'auto' : 'hidden';
}