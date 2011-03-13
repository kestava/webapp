// File: public-timeline.js

var kestava;

$(function() {
    // Start loading the public timeline
    // by default, we load the last 50 entries
    kestava.beginLoadTimeline(50);
});

kestava.beginLoadTimeline = function(maxEntries) {
    var url = 'http://kestava-timeline.jakewan.com/public?maxEntries=' + maxEntries + '&callback=?';
    $.getJSON(
        url,
        function(result) {
            alert(result);
        });
};