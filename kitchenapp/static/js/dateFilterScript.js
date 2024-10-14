function formatDateToYYYYMMDD(dateString) {
    // Create a new Date object from the input string
    const date = new Date(dateString);

    // Extract the year, month, and day components
    const year = date.getFullYear();
    const month = ("0" + (date.getMonth() + 1)).slice(-2); // Add leading zero for month if needed
    const day = ("0" + date.getDate()).slice(-2); // Add leading zero for day if needed

    // Return the formatted date in "yyyy-MM-dd" format
    return `${year}-${month}-${day}`;
}

// Generalized function to filter table rows based on date range
function filterTableByDateRange(table, dateFrom, dateTo) {
    const rows = table.querySelectorAll('tbody tr');

    rows.forEach(function(row) {
        const dateText = row.querySelector('.date').textContent.trim(); // Assuming dates are already in YYYY-MM-DD format
        const rowDate = new Date(dateText)

        // Compare date strings directly since YYYY-MM-DD can be compared lexicographically
        if (rowDate >= dateFrom.setHours(0) && rowDate <= dateTo.setHours(0)) {
            row.style.display = ''; // Show row
        } else {
            row.style.display = 'none'; // Hide row
        }
    });
}

// Generalized function to initialize date filtering for a table
function initializeDateFilter(table, dateFromInput, dateToInput) {
    const rows = table.querySelectorAll('tbody tr');

    let minDate = null;
    let maxDate = null;

    // Calculate the min and max dates in the table
    rows.forEach(function(row) {
        const dateText = row.querySelector('.date').textContent.trim();
        const rowDate = new Date(dateText)

        if (!minDate || rowDate < minDate) minDate = rowDate;
        if (!maxDate || rowDate > maxDate) maxDate = rowDate;
    });

    // Set default date range (one month back or minDate-maxDate range)
    const oneMonthAgo = new Date(maxDate);
    oneMonthAgo.setMonth(oneMonthAgo.getMonth() - 1);

    // Get one month ago in YYYY-MM-DD format
    const oneMonthAgoStr = oneMonthAgo.toISOString().split('T')[0];

    // Assign the correct date range without conversion to Date objects
    if (maxDate > minDate && maxDate > oneMonthAgoStr) { // More than 30 days apart
        dateFromInput.value = oneMonthAgoStr;
    } else {
        dateFromInput.value = formatDateToYYYYMMDD(minDate);
    }
    dateToInput.value = formatDateToYYYYMMDD(maxDate);

    // Filter table initially based on the default date range
    filterTableByDateRange(table, new Date(dateFromInput.value), new Date(dateToInput.value));

    // Add event listeners to update the table based on selected date range
    dateFromInput.addEventListener('change', function() {
        filterTableByDateRange(table, new Date(dateFromInput.value), new Date(dateToInput.value));
    });
    dateToInput.addEventListener('change', function() {
        filterTableByDateRange(table, new Date(dateFromInput.value), new Date(dateToInput.value));
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const tables = document.querySelectorAll('.with-date-filter');

    tables.forEach(function(table) {
        const tableId = table.getAttribute('data-table');

        // Find the associated date input fields for this table using the `data-table` attribute
        const dateFrom = document.querySelector(`.date-filter-from[data-table="${tableId}"]`);
        const dateTo = document.querySelector(`.date-filter-to[data-table="${tableId}"]`);
        initializeDateFilter(table, dateFrom, dateTo);
    });
});
