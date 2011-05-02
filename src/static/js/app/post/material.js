
$(function() {
    $('#itemsTable').dataTable({
        'bJQueryUI': true,
        'sPaginationType': 'full_numbers'
    });
    $('.buttonsContainer button').button();
    
    $('#copySelected, #editSelected').button('disable');
    
    $('#itemsTable > tbody > tr').click(
        function(ev) {
            var a = $(this);
            a.siblings('.row_selected').removeClass('row_selected');
            a.addClass('row_selected');
        });
});