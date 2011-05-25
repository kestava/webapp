/*!
 * app/account/add/newaccount.js
 */

var $, console;

$(function() {
    $('#firstName, #lastName, #userName')
        .val('')
        .formField();
    
    $('.buttonsContainer .submitButton').button({ disabled: true });
    $('.buttonsContainer .cancelButton').button();
    $('#checkAvail')
        .button()
        .click(function() {
            console.log('Checking availability...');
        });
});
