/*!
 * app/account/add/newaccount.js
 */

var $, console;

$(function() {
    
    var validateFirstName = function() {
            return (firstNameValid = (0 < $('#firstName').val().length));
        },
        validateLastName = function() {
            return (lastNameValid = (0 < $('#lastName').val().length));
        },
        validateUserName = function() {
            var val = $('#userName').val();
            
            if (1 > val.length) {
                return;
            }
            
            $('#checkAvail').siblings('.ajaxLoader, .errorMessage').remove().end()
                .after($(document.createElement('img'))
                    .attr('src', '/static/img/theme/smoothness/ajax-loader.gif')
                    .attr('alt', 'Working...')
                    .addClass('ajaxLoader'));
                
            $.ajax({
                url: '/services/checkusername',
                data: { 'username': val },
                success: function(data, status) {
                    var target = $('#userName'),
                        imageName,
                        message;
                    $('#checkAvail').siblings('.ajaxLoader, .errorMessage').remove();
                    if ('success' === status) {
                        imageName = true === data.available ? 'valid' : 'invalid';
                        message = true === data.available ? 'Username available' : 'Username already in use';
                        userNameValid = true === data.available ? true : false;
                    }
                    else {
                        imageName = 'invalid';
                        message = 'Error';
                        userNameValid = false;
                    }
                    target.formField('updateMessage', message, target.siblings(':last'));
                    target.formField('updateImage', imageName, target.siblings(':last'));
                    tryEnableCreateButton();
                },
                error: function() {
                    $('#checkAvail').siblings('.ajaxLoader, .errorMessage').remove().end()
                        .after($('<span class="errorMessage">Error</span>'));
                }
            });
        },
        tryEnableCreateButton = function() {
            $('.submitButton').button(firstNameValid && lastNameValid && userNameValid ? 'enable' : 'disable');
        },
        tryEnableCheckAvailButton = function() {
            $('#checkAvail').button(0 < $('#userName').val().length ? 'enable' : 'disable');
        },
        firstNameValid = false,
        lastNameValid = false,
        userNameValid = false;
    
    $('#firstName, #lastName, #userName')
        .val('')
        .formField();
    
    $('.buttonsContainer .submitButton').button({ disabled: true });
    $('.buttonsContainer .cancelButton').button();
    $('#checkAvail')
        .button()
        .click(function() {
            validateUserName();
        });
        
    $('#firstName').change(function() {
            var $t = $(this);
            $t.formField('updateImage', validateFirstName() ? 'valid' : 'invalid');
            tryEnableCreateButton();
        })
        .formField('setStateData', 'valid', '/static/img/silk/tick.png', 'First name is valid')
        .formField('setStateData', 'invalid', '/static/img/silk/asterisk_orange.png', 'First name is invalid');
    
    $('#lastName').change(function() {
            var $t = $(this);
            $t.formField('updateImage', validateLastName() ? 'valid' : 'invalid');
            tryEnableCreateButton();
        })
        .formField('setStateData', 'valid', '/static/img/silk/tick.png', 'Last name is valid')
        .formField('setStateData', 'invalid', '/static/img/silk/asterisk_orange.png', 'Last name is invalid');
        
    $('#userName').keyup(function() {
        tryEnableCheckAvailButton();
    });

    tryEnableCheckAvailButton();
});

app.utilities.preloadImages([
    '/static/img/theme/smoothness/ajax-loader.gif',
    '/static/img/silk/tick.png',
    '/static/img/silk/asterisk_orange.png']);
