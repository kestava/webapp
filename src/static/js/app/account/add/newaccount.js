/*!
 * app/account/add/newaccount.js
 */

$(function() {
    var createButton = $('.buttonsContainer .submitButton');
    
    $('#firstName, #lastName, #userName').val('');
    
    $('#firstName').formField({
        'required': true,
        'submitButton': createButton
    });
    $('#lastName').formField({
        'required': false
    });
    $('#userName').formField({
        'required': true,
        'submitButton': createButton
    });
    
    createButton.button({ disabled: true });
    $('.buttonsContainer .cancelButton').button();
});