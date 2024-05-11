let selectedProductId = null;
let selectedLocationId = null;

//document.getElementById('submit-addproduct').addEventListener('click', function() {
//
//    if (selectedProductId) {
//        const selectedLocations = Array.from(document.querySelectorAll('#location-stock-container .selectable.selected'))
//            .map(cell => cell.getAttribute('data-locationid'));
//
//        console.log(`Adding product ${selectedProductId} to locations ${selectedLocations.join(', ')}`);
//        let userid = sessionStorage.getItem("userid");
//
//        eel.addProductToLocations(selectedProductId, selectedLocations)(response => {
//           if (response) {
//                console.log('Product added successfully, reloading page...');
//                console.log("userid", userid)
//                eel.addProductToInorders(selectedProductId, selectedLocations, parseInt(userid))
//                window.location.reload();
//            } else {
//                console.log('Failed to add product to locations.');
//            }
//        });
//    } else {
//        console.log('Please select a product.');
//    }
//});

function productCellClicked(cell) {
    // ยกเลิกการเลือกสินค้าที่เคยเลือกไว้ก่อนหน้านี้
    const previouslySelectedProduct = document.querySelector('#stock-product-container .selectable.selected');
    if (previouslySelectedProduct) {
        previouslySelectedProduct.classList.remove('selected');
    }
    // เลือกสินค้าใหม่
    cell.classList.add('selected');
    selectedProductId = cell.getAttribute('data-productid');
    console.log(`Selected product ID: ${selectedProductId}`);
}


function cellClicked(cell) {
    // ตรวจสอบว่า cell ที่คลิกถูกเลือกอยู่หรือไม่
    const isSelected = cell.classList.contains('selected');

    // ดึงทุก cell ที่ถูกเลือก
    const allSelectedCells = document.querySelectorAll('#location-stock-container .selectable.selected');

    // ยกเลิกการเลือกทุก cell ที่ถูกเลือก
    allSelectedCells.forEach(selectedCell => {
        selectedCell.classList.remove('selected');
    });

    // เพิ่มการเลือกให้กับ cell ที่คลิกถ้ามันไม่ได้ถูกเลือกอยู่ก่อน
    if (!isSelected) {
        cell.classList.add('selected');
        selectedLocationId = cell.getAttribute('data-locationid');
    } else {
        selectedLocationId = null;
    }
}

//function cellClicked(cell) {
//    const isSelected = cell.classList.contains('selected');
//    const allSelectedCells = document.querySelectorAll('#location-stock-container .selectable.selected');
//    allSelectedCells.forEach(selectedCell => {
//        selectedCell.classList.remove('selected');
//    });
//    if (!isSelected) {
//        cell.classList.add('selected');
//        selectedLocationId = cell.getAttribute('data-locationid');
//    } else {
//        selectedLocationId = null;
//    }
//}


//function cellClicked(cell) {
//    // Toggle การเลือกตำแหน่งโดยไม่ลบการเลือกก่อนหน้า
//    cell.classList.toggle('selected');
//    const isSelected = cell.classList.contains('selected');
//    const locationid = cell.getAttribute('data-locationid');
//    console.log(`Location ID ${locationid} is now ${isSelected ? 'selected' : 'not selected'}`);
//}
