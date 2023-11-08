const item = document.getElementById("lenItem");
const value = parseInt(item.className)

for (var i=1;i<value;i++) {
    const item = document.getElementById(`${i}`);
    const alert = document.getElementById(`alerts_count_${i}`);
    console.log(alert)
    // const alertsValue = document.getElementById(`alerts_count_2`);
    if (alert == null) {
        item.style.borderLeft = "#2EDD94 solid 15px";
    } else {
        item.style.borderLeft = "#d35252 solid 15px";
    }
}