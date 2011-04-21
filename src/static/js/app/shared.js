/*!
 * shared.js
 */

var app;

$(function() {
    var a = app.classes.topbar,
        b = function(a, b, c, d) {
            var tb = app.classes.topbar;
            a.hover(
                tb.mouseEnterDropDown(b, a),
                tb.mouseLeaveDropDown(b, a, c));
            d.click(tb.dropDownHeaderClicked(b, a, c));
        };
    
    b($('#sessionContainer'),
        $('#sessionContainer .dropDown'),
        'stickySessionAreaOpen',
        $('#nameContainer'));
    
    b($('#postNavContainer'),
        $('#postNavContainer .dropDown'),
        'stickyPostNavDropDownOpen',
        $('#postNavContainer > p'));
    
    b($('#manageNavContainer'),
        $('#manageNavContainer .dropDown'),
        'stickyManageNavDropDownOpen',
        $('#manageNavContainer > p'));
    
    b($('#followNavContainer'),
        $('#followNavContainer .dropDown'),
        'stickyFollowNavDropDownOpen',
        $('#followNavContainer > p'));
    
});

app.classes.topbar = (function() {
    return {
        stickySessionAreaOpen: false,
        stickyPostNavDropDownOpen: false,
        stickyManageNavDropDownOpen: false,
        stickyAnalysisNavDropDownOpen: false,
        mouseEnterDropDown: function(a, b) {
            return function(ev) {
                a.show();
                b.addClass('open');
            };
        },
        mouseLeaveDropDown: function(a, b, c) {
            return function(ev) {
                var tb = app.classes.topbar;
                if (!tb[c]) {
                    a.hide();
                    b.removeClass('open');
                }
            };
        },
        dropDownHeaderClicked: function(a, b, c) {
            return function(ev) {
                var tb = app.classes.topbar;
                if (tb[c]) {
                    a.hide();
                    b.removeClass('open');
                }
                else {
                    a.show();
                    b.addClass('open');
                }
                tb[c] = !tb[c];
            };
        }
    };
}());