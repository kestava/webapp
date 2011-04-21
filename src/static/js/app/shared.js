/*!
 * shared.js
 */

var app;

$(function() {
    var a = app.classes.topbar,
        b = function(a, b, c, d) {
            var tb = app.classes.topbar;
            a.hover(
                tb.mouseEnterDropDown(b, a, c),
                tb.mouseLeaveDropDown(b, a, c));
            d.click(tb.dropDownHeaderClicked(b, a, c));
        };
    
    b($('#sessionContainer'),
        $('#sessionContainer .dropDown'),
        'sessionArea',
        $('#nameContainer'));
    
    b($('#postNavContainer'),
        $('#postNavContainer .dropDown'),
        'postNavDropDown',
        $('#postNavContainer > p'));
    
    b($('#manageNavContainer'),
        $('#manageNavContainer .dropDown'),
        'manageNavDropDow',
        $('#manageNavContainer > p'));
    
    b($('#followNavContainer'),
        $('#followNavContainer .dropDown'),
        'followNavDropDown',
        $('#followNavContainer > p'));
    
});

app.classes.topbar = (function() {
    return {
        stickyOpenDropDown: null,
        mouseEnterDropDown: function(a, b, c) {
            return function(ev) {
                var tb = app.classes.topbar;
                
                if (tb.stickyOpenDropDown !== c) {
                    tb.stickyOpenDropDown = null;
                }
                $('.dropDownContainer.open .dropDown').hide();
                $('.dropDownContainer').removeClass('open');
                
                a.show();
                b.addClass('open');
            };
        },
        mouseLeaveDropDown: function(a, b, c) {
            return function(ev) {
                var tb = app.classes.topbar;
                if (tb.stickyOpenDropDown !== c) {
                    a.hide();
                    b.removeClass('open');
                }
            };
        },
        dropDownHeaderClicked: function(a, b, c) {
            return function(ev) {
                var tb = app.classes.topbar;
                if (tb.stickyOpenDropDown === c) {
                    tb.stickyOpenDropDown = null;
                    a.hide();
                    b.removeClass('open');
                }
                else {
                    tb.stickyOpenDropDown = c;
                    a.show();
                    b.addClass('open');
                }
            };
        }
    };
}());