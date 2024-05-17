$(document).ready(function() {
    // Inicializar DataTable
    var table = $('#queriesTable').DataTable({
        columnDefs: [
            { type: 'num', targets: [2, 3, 4] }
        ],
        order: [[4, 'desc']],
        autoWidth: false,
        responsive: true,
        fixedHeader: true,
        columns: [
            { width: '10%' },
            { width: '50%' },
            { width: '8%' },
            { width: '8%' },
            { width: '8%' },
            { width: '8%' },
            { width: '8%' }
        ]
    });

    $('.query-row').click(function(e) {
        var $this = $(this);
        var fullQueryRow = $this.next('.full-query-row');
        fullQueryRow.toggle();
    });

    // Manejar cambio en el filtro de usuario
    $('#user-filter').on('change', function() {
        var user = $.fn.dataTable.util.escapeRegex(this.value);
        table.column(6).search(user ? '^' + user + '$' : '', true, false).draw();
    });

    // Manejar cambio en el filtro de base de datos
    $('#database-filter').on('change', function() {
        var database = $.fn.dataTable.util.escapeRegex(this.value);
        table.column(5).search(database ? '^' + database + '$' : '', true, false).draw();
    });

    // Manejar clic en botón de Refresh
    $('#refresh-btn').on('click', function() {
        $('#loadingModal').modal('show');
        $.ajax({
            url: '/',
            type: 'POST',
            data: { 'queries': true },
            dataType: 'json',
            success: function(data) {
                // Limpiar la tabla
                table.clear();
                
                // Agregar las filas de datos
                for (var i = 0; i < data.length; i++) {
                    var rowData = data[i];
                    var rowHtml = '<tr class="query-row">' +
                        '<td>' + rowData[0] + '</td>' +
                        '<td class="text-nowrap overflow-hidden" style="max-width: 0;">' +
                            '<details>' +
                                '<summary>' +
                                    '<span class="short-query">' +
                                        rowData[1] +
                                    '</span>' +
                                '</summary>' +
                                '<pre style="font-family: monospace; white-space: pre-wrap; word-wrap: break-word;">' + rowData[1] + '</pre>' +
                            '</details>' +
                        '</td>' +
                        '<td>' + rowData[2] + '</td>' +
                        '<td>' + rowData[3] + '</td>' +
                        '<td>' + rowData[4] + '</td>' +
                        '<td>' + rowData[5] + '</td>' +
                        '<td>' + rowData[6] + '</td>' +
                    '</tr>';
                    table.row.add($(rowHtml)).draw();
                }
                $('#loadingModal').modal('hide');
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
                $('#loadingModal').modal('hide');
            }
        });
    });

    // Manejar clic en fila para mostrar la consulta completa
    $('#queriesTable tbody').click(function(e) {
        var $this = $(this);
        var fullQueryRow = $this.next('.full-query-row');
        fullQueryRow.toggle();
    });


    // Manejar clic en botón de Reset
    $('#reset-btn').on('click', function() {
        $.ajax({
            url: '/',
            type: 'POST',
            data: { 'reset': true },
            success: function() {
                table.clear().draw();
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
            }
        });
    });

});
