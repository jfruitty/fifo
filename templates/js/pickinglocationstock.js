let selectedLocationIds = [];
let selectedProductIdAdd = null;

//document.getElementById('submit-pickproduct').addEventListener('click', function() {
//    const selectedLocations = selectedLocationIds; // หรือ Array.from(document.querySelectorAll('#location-stock-container .selectable.selected'))
////    console.log(`locations Pick ${selectedLocations} ${selectedProductIdAdd}`);
//    eel.pickProductToLocations(selectedLocations)(response => {
//        if(response){
//            let userid = sessionStorage.getItem("userid");
//            console.log("userid",userid)
//            eel.pickProductToInorders(parseInt(selectedProductIdAdd), selectedLocationIds, userid)
//            window.location.reload();
//
//        }else{
//            console.log('Feid pickProductToLocations')
//        }
//
//    });
//
//});

function cellClicked(cell) {
    const locationid = cell.getAttribute('data-locationid');
    const row = cell.getAttribute('data-row');
    const column = cell.getAttribute('data-column');
    selectedProductIdAdd = cell.getAttribute('data-productid'); // Capture product ID when clicking a cell
    cell.classList.toggle('selected');

    if (cell.classList.contains('selected')) {
        selectedLocationIds.push(locationid);
        cell.style = "background-color: rgb(255, 215, 0)";
    } else {
        selectedLocationIds = selectedLocationIds.filter(id => id !== locationid);
        cell.style = "";
    }


    console.log(`Location ID Pick ${locationid} is now ${cell.classList.contains('selected') ? 'selected' : 'not selected'} `);
}


