/*!
 * shared.js
 */

var app;

$(function() {
    var a = app.classes.topbar;
    a.sessionContainer = $('#sessionContainer');
    a.sessionContainerDropDown = $('#sessionContainer .dropDown');
    $('#sessionContainer').hover(a.onUserAreaMouseEnter, a.onUserAreaMouseLeave);
    $('#nameContainer').click(a.nameContainerClicked);
});

app.classes.topbar = (function() {
    return {
        stickySessionAreaOpen: false,
        onUserAreaMouseEnter: function(ev) {
            var a = app.classes.topbar;
            a.sessionContainerDropDown.show();
            a.sessionContainer.addClass('open');
        },
        onUserAreaMouseLeave: function(ev) {
            var a = app.classes.topbar
            if (!a.stickySessionAreaOpen) {
                a.sessionContainerDropDown.hide();
                a.sessionContainer.removeClass('open');
            }
        },
        nameContainerClicked: function(ev) {
            var a = app.classes.topbar;
            if (a.stickySessionAreaOpen) {
                a.sessionContainerDropDown.hide();
                a.sessionContainer.removeClass('open');
            }
            else {
                a.sessionContainerDropDown.show();
                a.sessionContainer.addClass('open');
            }
            a.stickySessionAreaOpen = !a.stickySessionAreaOpen;
        }
    };
}());