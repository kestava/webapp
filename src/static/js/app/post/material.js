/*!
 * material.js
 */

var app, $;

$(function() {
    $('#itemsTable').dataTable({
        'bJQueryUI': true,
        'sPaginationType': 'full_numbers'
    });
    $('.buttonsContainer button').button();
    
    $('#copySelected, #editSelected').button('disable');
    
    $('#createNew').click(function() {
        app.classes.material_post.createNew();
    });
    
    $('#editSelected').click(function() {
        app.classes.material_post.editSelected();
    });
    
    $('#copySelected').click(function() {
        app.classes.material_post.copySelected();
    });
    
    $('#itemsTable > tbody > tr').click(
        function() {
            var a = $(this),
                b = $('.dataTables_empty', a);
            
            if (0 === b.length) {
                a.siblings('.row_selected').removeClass('row_selected');
                if (a.hasClass('row_selected')) {
                    a.removeClass('row_selected');
                }
                else {
                    a.addClass('row_selected');
                }
                app.classes.material_post.updateOptButtons();
            }
        });
});

app.classes.material_post = (function() {
        
    return {
        updateOptButtons: function() {
            var a = $('#itemsTable > tbody > tr.row_selected'),
                b =  (0 === a.length) ? 'disable' : 'enable',
                c = $('#copySelected, #editSelected');
            c.button(b);
        },
        createNew: function() {
            $('#optionForm').attr('action', '/post/material/create');
        },
        copySelected: function() {
            $('#optionForm').attr('action', '/post/material/copy/itemid');
        },
        editSelected: function() {
            $('#optionForm')
                .attr('method', 'get')
                .attr('action', '/myusername/itemid/edit');
        }
    };
}());