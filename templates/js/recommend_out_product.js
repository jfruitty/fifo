let LocationIds = [];
let selectedAutoProductId = null;
let unitsToAddAuto = 0;
let ProductID = [];
document.addEventListener('DOMContentLoaded', function () {
    // เติม dropdown ด้วยข้อมูลสินค้า
    eel.fetch_product_data()(function (products) {
        const dropdown = document.getElementById('product-dropdown-out');
        products.forEach((product) => {
            const option = document.createElement('option');
            option.value = product.productid;
            option.textContent = `${product.productname}`;
            dropdown.appendChild(option);
        });
    });

    const pickProductButton = document.getElementById(
        'submit-pickproduct-action'
    );

    if (pickProductButton) {
        pickProductButton.addEventListener('click', function () {
            const selectedProductId = document.getElementById(
                'product-dropdown-out'
            ).value;
            const unitsToPick =
                parseInt(
                    document.getElementById('product-out-unit').value,
                    10
                ) || 1;
            console.log(
                `Selected product Picking: ${selectedProductId}, units: ${unitsToPick}`
            );

            eel.get_oldest_product(
                parseInt(unitsToPick),
                parseInt(selectedProductId)
            )(function (oldestProducts) {
                console.log('Oldest Products:', oldestProducts);

                oldestProducts.forEach((product) => {
                    const cell = document.querySelector(
                        `[data-locationid='${product.locationid}']`
                    );
                    if (cell) {
                        cell.style.backgroundColor = '#FFD700';
                        LocationIds.push(product.locationid);
                        ProductID.push(product.productid);
                    }
                });
            });
        });
    }
    console.log(LocationIds);
    const pickProductAuto = document.getElementById('submit-pickproduct-auto');
    if (pickProductAuto) {
        LocationIds = [];
        pickProductAuto.addEventListener('click', function () {
            console.log(`Locations to Pick: ${LocationIds}`);
            let userid = sessionStorage.getItem('userid');
            console.log('ProductID', ProductID[0]);
            eel.pickProductToLocations(LocationIds)((response) => {
                if (response) {
                    eel.pickProductToInorders(
                        parseInt(ProductID[0]),
                        LocationIds,
                        parseInt(userid)
                    );
                    window.location.reload(); // รีเฟรชเมื่อสำเร็จ
                } else {
                    console.log('ไม่สามารถเบิกสินค้าได้');
                }
            });
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    // เติม dropdown ด้วยข้อมูลสินค้า
    eel.fetch_product_data()(function (products) {
        const dropdown = document.getElementById('product-dropdown-in');
        products.forEach((product) => {
            const option = document.createElement('option');
            option.value = product.productid;
            option.textContent = `${product.productname}`;
            dropdown.appendChild(option);
        });
    });

    const addProductButton = document.getElementById(
        'submit-addingproduct-action'
    );
    if (addProductButton) {
        addProductButton.addEventListener('click', function () {
            selectedAutoProductId = document.getElementById(
                'product-dropdown-in'
            ).value;
            unitsToAddAuto =
                parseInt(
                    document.getElementById('product-in-unit').value,
                    10
                ) || 1;
            console.log(
                `Adding Product Marker: ${selectedAutoProductId}, Units: ${unitsToAddAuto}`
            );

            eel.mark_location_adding(
                selectedAutoProductId,
                unitsToAddAuto
            )(function (locations) {
                LocationIds = locations; // จัดเก็บสถานที่ใน LocationIds เพื่อการใช้ในภายหลัง
                locations.forEach((locationid) => {
                    const cell = document.querySelector(
                        `[data-locationid='${locationid}']`
                    );
                    if (cell) {
                        cell.style.backgroundColor = '#FFD700'; // ไฮไลท์ตำแหน่งนี้
                    }
                });
            });
        });
    }

    const addingProductAuto = document.getElementById('submit-addproduct-auto');
    if (addingProductAuto) {
        addingProductAuto.addEventListener('click', function () {
            console.log(
                `Auto-Adding Product: ${selectedAutoProductId}, Units: ${unitsToAddAuto}`
            );

            eel.auto_adding_location_product(
                parseInt(selectedAutoProductId),
                parseInt(unitsToAddAuto)
            )(function (response) {
                console.log('Auto Adding Location Product Response:', response);
                let userid = sessionStorage.getItem('userid');
                eel.addProductToInorders(
                    parseInt(selectedAutoProductId),
                    LocationIds,
                    parseInt(userid)
                );
                if (response) {
                    window.location.reload(); // รีเฟรชเมื่อสำเร็จ
                } else {
                    console.log('ไม่สามารถเบิกสินค้าได้');
                }
            });
        });
    }
});

// Clear the selection when the quantity control or product ID dropdown is changed
// Assuming the quantity control's id is "product-out-unit" and the product ID dropdown's id is "product-dropdown-out"

let productQtyControl = document.getElementById('product-out-unit');
let productIdControl = document.getElementById('product-dropdown-out');
let productQtyControlIn = document.getElementById('product-in-unit');
let productIdControlIn = document.getElementById('product-dropdown-in');

// Event listener for quantity control
productQtyControl.addEventListener('input', function () {
    clearSelection();
});
productQtyControlIn.addEventListener('input', function () {
    clearSelection();
});

// Event listener for product ID dropdown
productIdControl.addEventListener('change', function () {
    clearSelection();
});
productIdControlIn.addEventListener('change', function () {
    clearSelection();
});

// Function to clear the selection
function clearSelection() {
    LocationIds.length = 0;
    ProductID.length = 0;
    // Reset the background color of all cells
    let cells = document.querySelectorAll('[data-locationid]');
    cells.forEach((cell) => (cell.style.backgroundColor = ''));
}
