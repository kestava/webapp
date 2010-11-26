var kestava;

$(function() {
    $('#providerGoogle').click(function(ev) {
        kestava.onProviderClick('google');
    });
    
    $('#providerYahoo').click(function(ev) {
        kestava.onProviderClick('yahoo');
    });
});

kestava.onProviderClick = function(providerName) {
    var infoTextDiv = $('#infoTextContainer');
    
    $('#chosenProviderName').val(providerName);
    
    infoTextDiv.children().remove();
    kestava.providerInfo[providerName].createInfoText(infoTextDiv);
    
    $('#providerInfoPanelContainer:hidden').fadeIn('fast');
};

kestava.addParagraph = function(parent, text) {
    var a = $(document.createElement('p'));
    a.text(text);
    parent.append(a);
}

kestava.providerInfo = (function() {
    return {
        'google': {
            'createInfoText': function(parent) {
                kestava.addParagraph(parent, 'Click the "Go" button to login using your Google account.');
                kestava.addParagraph(parent, 'You may be redirected to a secure Google page for authentication.');
            }
        },
        'yahoo': {
            'createInfoText': function(parent) {
                kestava.addParagraph(parent, 'Click the "Go" button to login using your Yahoo! account.');
                kestava.addParagraph(parent, 'You may be redirected to a secure Yahoo! page for authentication.');
            }
        }
    };
})();