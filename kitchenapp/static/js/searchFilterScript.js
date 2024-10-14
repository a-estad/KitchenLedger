function initializeSearchFilter(table, searchInput) {
    searchInput.addEventListener('keyup', function () {
        const rows = table.querySelectorAll('tbody tr');

        rows.forEach(function (row) {
            const fields = row.querySelectorAll('td');
            let rowString = '';
            fields.forEach(field => {
                rowString += field.textContent.toLowerCase();
            });

            if (rowString.includes(searchInput.value.toLowerCase())) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const tables = document.querySelectorAll('.with-search-filter');

    tables.forEach(function(table) {
        const tableId = table.getAttribute('data-table');

        // Find the associated date input fields for this table using the `data-table` attribute
        const searchInput = document.querySelector(`.search-filter[data-table="${tableId}"]`);
        initializeSearchFilter(table, searchInput);
    });

});
