/*!
 * shared.js
 */

var app;

$(function() {
    var b = function(a, b, c, d) {
            var tb = app.classes.header;
            a.hover(
                tb.mouseEnterDropDown(b, a, c),
                tb.mouseLeaveDropDown(b, a, c));
            d.click(tb.dropDownHeaderClicked(b, a, c));
        };
    
    $('#homeLinkContainer').mouseenter(function(ev) {
        app.classes.header.hideDropDowns();
    });
    
    b($('#postNavContainer'),
        $('#postNavContainer nav'),
        'post',
        $('#postNavContainer > h1'));
    
    b($('#manageNavContainer'),
        $('#manageNavContainer nav'),
        'manage',
        $('#manageNavContainer > h1'));
    
    b($('#followNavContainer'),
        $('#followNavContainer nav'),
        'follow',
        $('#followNavContainer > h1'));
    
    if (1 == $('#sessionContainer nav').length) {
        b($('#sessionContainer'),
            $('#sessionContainer nav'),
            'session',
            $('#nameContainer'));
    }
});

app.classes.header = (function() {
    return {
        stickyOpenDropDown: null,
        hideDropDowns: function() {
            $('.headingContainer nav').hide();
            $('.headingContainer').removeClass('open');
        },
        mouseEnterDropDown: function(a, b, c) {
            return function(ev) {
                var tb = app.classes.header;
                
                if (tb.stickyOpenDropDown !== c) {
                    tb.stickyOpenDropDown = null;
                }
                tb.hideDropDowns();
                
                a.show();
                b.addClass('open');
            };
        },
        mouseLeaveDropDown: function(a, b, c) {
            return function(ev) {
                var tb = app.classes.header;
                if (tb.stickyOpenDropDown !== c) {
                    a.hide();
                    b.removeClass('open');
                }
            };
        },
        dropDownHeaderClicked: function(a, b, c) {
            return function(ev) {
                var tb = app.classes.header;
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

if ("onpagehide" in window) {
    // This event handler plays nice with the back/forward buttons in some
    // browsers (WebKit ones mainly).
    window.addEventListener(
        "pageshow",
        function(ev) {
            if (ev.persisted) {
                $('.headingContainer nav').hide();
                $('.headingContainer').removeClass('open');
            }
        },
        false);
}
