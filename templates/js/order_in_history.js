let currentPage = 1;
const ordersPerPage = 10;

document.addEventListener('DOMContentLoaded', function() {
    eel.fetch_order_in_history()(function(orders) {
        const container = document.getElementById('order-history-container');
        updateTable(orders, container);
    });
});

function updateTable(orders, container) {
    let table = '<table>';
    table += '<tr><th>รายการ</th><th>ผู้ใช้</th><th>สินค้า</th><th>จำนวน</th><th>วันที่</th></tr>';
    const startIdx = (currentPage - 1) * ordersPerPage;
    const endIdx = Math.min(startIdx + ordersPerPage, orders.length);

    for (let i = startIdx; i < endIdx; i++) {
        const order = orders[i];
        table += `
            <tr>
                <td>${i + 1}</td>
                <td>${order[2]}</td>
                <td>${order[3]}</td>
                <td>${order[4]}</td>
                <td>${order[5]}</td>
            </tr>`;
    }

    for (let i = endIdx; i < startIdx + ordersPerPage; i++) {
        table += `
            <tr>
                <td>${i + 1}</td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
            </tr>`;
    }

    table += '</table>';
    container.innerHTML = table;

    // Add pagination controls
    updatePaginationControls(container, orders.length);
}

function updatePaginationControls(container, totalOrders) {
    const totalPages = Math.ceil(totalOrders / ordersPerPage);
    let paginationControls = '<div class="pagination">';

    for (let page = 1; page <= totalPages; page++) {
        paginationControls += `<button class="page-btn" onclick="goToPage(${page})">${page}</button>`;
    }

    paginationControls += '</div>';
    container.innerHTML += paginationControls;
}

function goToPage(page) {
    currentPage = page;
    const container = document.getElementById('order-history-container');
    eel.fetch_order_in_history()(function(orders) {
        updateTable(orders, container);
    });
}
