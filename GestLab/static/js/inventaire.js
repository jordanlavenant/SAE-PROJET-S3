const item = document.getElementById("lenItem");
const value = parseInt(item.className)

for (let i=1;i<=8;i++) {
    if (document.getElementById(`item_${i}`) != null) {
        if (document.getElementById(`alerts_count_${i}`) != null) {
            document.getElementById(`item_${i}`).style.borderLeft = "#d35252 solid 15px";
        } else {
            document.getElementById(`item_${i}`).style.borderLeft = "#2EDD94 solid 15px";
        }
    }
}