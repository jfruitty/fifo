document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('add-product-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const productname = document.getElementById('productname').value;
        const productno = document.getElementById('productno').value;
        const productqty = document.getElementById('productqty').value;
        const productunit = document.getElementById('productunit').value;

        eel.add_product(productname, productno, productqty, productunit)(function(response) {
            if (response) {
                console.log('Product added successfully');
                window.location.reload();
            } else {
                console.log('Failed to add product');
            }
        });
    });
});
document.addEventListener('DOMContentLoaded', function() {
    eel.fetch_product_data()(populateTable);

    function populateTable(products) {
        const tableBody = document.getElementById('product-table').getElementsByTagName('tbody')[0];
        products.forEach((product) => {
            const row = tableBody.insertRow();
            row.innerHTML = `
                <td>${product.productid}</td>
                <td contenteditable="true" data-field="productname">${product.productname}</td>
                <td contenteditable="true" data-field="productno">${product.productno}</td>
                <td contenteditable="true" data-field="productqty">${product.productqty}</td>
                <td contenteditable="true" data-field="productunit">${product.productunit}</td>
                <td><button onclick="updateProduct(this)">Update</button></td>
            `;
        });
    }

    window.updateProduct = function(button) {
        const row = button.parentNode.parentNode;
        const productid = row.cells[0].innerText;
        const productname = row.cells[1].innerText;
        const productno = row.cells[2].innerText;
        const productqty = row.cells[3].innerText;
        const productunit = row.cells[4].innerText;

        eel.update_product_details(productid, productname, productno, productqty, productunit)((response) => {
            if (response) {
                alert('Product updated successfully.');
            } else {
                alert('Failed to update product.');
            }
        });
    };
});
