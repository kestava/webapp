/*!
 * login.js
 */

app.classes.login = (function() {
    return {
        onClickProvider: function(ev) {
            var authType = $('input.authType', this).val(),
                authUrl = $('input.authUrl', this).val();
            
            $('#loginForm input[name=provider]').remove();
            $('#loginForm input[name=authType]').remove();
            $('#loginForm input[name=authUrl]').remove();
            
            $('#loginForm > div')
                .append(
                    $(document.createElement('input'))
                        .attr('type', 'hidden')
                        .attr('name', 'provider')
                        .attr('value', this.id))
                .append(
                    $(document.createElement('input'))
                        .attr('type', 'hidden')
                        .attr('name', 'authType')
                        .attr('value', authType))
                .append(
                    $(document.createElement('input'))
                        .attr('type', 'hidden')
                        .attr('name', 'authUrl')
                        .attr('value', authUrl));
                
            $('#loginForm').submit();
        }
    };
}());
 
$(function() {
    $('#loginForm li').click(app.classes.login.onClickProvider);
});