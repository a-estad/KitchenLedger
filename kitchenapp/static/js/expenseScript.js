document.addEventListener('DOMContentLoaded', function() {
    const table = document.getElementById('expensesTable');
    const deleteButton = document.getElementById('deleteButton');
    let selectedRows = [];

    // Add click event listeners to each table row
    table.querySelectorAll('tbody tr.data').forEach(function(row) {
        row.addEventListener('click', function() {
            const selectedExpenseId = row.getAttribute('data-id');
            if (row.classList.contains('table-active-custom')) {
                // Deselect the row
                row.classList.remove('table-active-custom');
                // Remove from the selected rows array
                selectedRows = selectedRows.filter(id => id !== selectedExpenseId);
            } else {
                // Select the row
                row.classList.add('table-active-custom');
                // Add the row's expense ID to the selected rows array
                selectedRows.push(selectedExpenseId);
            }

            // Update the delete button visibility and hidden input
            if (selectedRows.length > 0) {
                deleteButton.style.display = 'inline-block';
                document.getElementById('hiddenExpenseId').value = selectedRows.join(',');  // Store as comma-separated values
            } else {
                deleteButton.style.display = 'none';
                document.getElementById('hiddenExpenseId').value = '';  // Clear if no selection
            }
        });
    });
});