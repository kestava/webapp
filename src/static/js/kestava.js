
$(function() {
    $('#userGreetingArea').click(kestava.userGreetingAreaClick);
});

var kestava = (function() {
    return {
        'userGreetingAreaClick': function (ev) {
            $('#userMenu').fadeToggle('fast');
        }
    };
})();