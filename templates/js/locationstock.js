

function createTable(locations) {
    const container = document.getElementById('location-stock-container');
    let table = '<table>';
    table += '<tr><th>No</th>';

    const members = [
        'E10', 'E9', 'E8', 'E7', 'E6', 'E5', 'E4', 'E3', 'E2', 'E1',
        'D10', 'D9', 'D8', 'D7', 'D6', 'D5', 'D4', 'D3', 'D2', 'D1',
        'C10', 'C9', 'C8', 'C7', 'C6', 'C5', 'C4', 'C3', 'C2', 'C1',
        'B3', 'B2', 'B1'
    ];

    members.forEach(member => table += `<th>${member}</th>`);
    table += '</tr>';

    for (let row = 1; row <= 16; row++) { // แถวจาก 1 ถึง 16
        table += `<tr><td>${row}</td>`;
        for (let col = 33; col >= 1; col--) { // คอลัมน์จาก 33 ถึง 1
            const locationIndex = locations.findIndex(loc => loc['row'] == row && loc['column'] == col);
            if (locationIndex >= 0) {
                const location = locations[locationIndex];
                const isSelected = location['productid'] ? 'selected' : '';
                const groupClass = location['groupNo'] ? `group-${location['groupNo']}` : '';
                table += `<td class='selectable ${isSelected} ${groupClass}' data-row='${row}' data-column='${col}' data-productid='${location['productid'] || ''}' data-locationid='${location['locationid']}' onclick='cellClicked(this)'>${location['productid'] || ' '}</td>`;

                //console.log(`Row: ${row}, Column: ${col}, GroupNo: ${location['groupNo']}`);

            } else {
                table += `<td></td>`;
            }
        }
        table += '</tr>';
    }
    container.innerHTML = table;
}


//function createTableProduct(products) {
//    const container = document.getElementById('stock-product-container');
//    let table = '<table class="product">';
//    // Generate the headers for each column set
//    table += '<tr>';
//    for (let col = 0; col < 1; col++) {
//        table += '<th>No</th><th>Product Name</th><th>Quantity</th><th>Unit</th>';
//    }
//    table += '</tr>';
//
//  for (let row = 0; row < 5; row++) {
//        table += '<tr>';
//
//            const productIndex =  row;
//            const product = products[productIndex] || { productid: ' ', productno: ' ', productname: ' ', productqty: ' ', productunit: ' ' };
//            table += `<td class='selectable' onclick='productCellClicked(this)' data-productid='${product.productid}' data-productno='${product.productno}' data-productname='${product.productname}' data-productqty='${product.productqty}' data-unit='${product.productunit}'>${product.productid}</td>`;
//            table += `<td>${product.productname}</td>`;
//            table += `<td>${product.productqty}</td>`;
//            table += `<td>${product.productunit}</td>`;
//
//        table += '</tr>';
//    }
//
//    table += '</table>';
//    container.innerHTML = table;
//}


document.addEventListener('DOMContentLoaded', function() {
    eel.fetch_location_data()(createTable);
    // eel.fetch_product_data()(createTableProduct);
});

//window.onload = function() {
//   if (document.documentElement.requestFullscreen) {
//     document.documentElement.requestFullscreen();
//   } else if (document.documentElement.webkitRequestFullscreen) { /* Safari */
//     document.documentElement.webkitRequestFullscreen();
//   } else if (document.documentElement.mozRequestFullScreen) { /* Firefox */
//     document.documentElement.mozRequestFullScreen();
//   } else {
//     // Handle cases where full screen is not supported
//   }
// };