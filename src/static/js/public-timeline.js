// File: public-timeline.js

var kestava;

$(function() {
    // Start loading the public timeline
    // by default, we load the last 50 entries
    kestava.beginLoadTimeline(50);
});

kestava.beginLoadTimeline = function(maxEntries) {
    //var url = 'http://kestava-timeline.jakewan.com/public?maxEntries='
    var url = 'http://' + kestava.timelineServerHostname + '/public?maxEntries='
        + maxEntries + '&callback=?';
        
    $.getJSON(url, kestava.endLoadTimeline);
};

kestava.endLoadTimeline = function(result) {
    var i, o, dt, jake;
    for (i in result)
    {
        if (result.hasOwnProperty(i))
        {
            o = result[i];
            dt = kestava.iso_8601_to_date(o.created_when_formatted);
            jake = 0;
        }
    }
};