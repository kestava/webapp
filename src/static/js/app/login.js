/*!
 * login.js
 */

app.classes.login = (function() {
    return {
        onClickProvider: function(ev) {
            $('#loginForm input[name=provider]').remove();
            $('#loginForm')
                .append(
                    $(document.createElement('input'))
                        .attr('type', 'hidden')
                        .attr('name', 'provider')
                        .attr('value', this.id))
                .submit();
        }
    };
}());
 
$(function() {
    $('#loginForm li').click(app.classes.login.onClickProvider);
});