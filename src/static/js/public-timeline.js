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
    var i, o, p, dt,
        container = $('#innerContainer'),
        jake;
    for (i in result)
    {
        if (result.hasOwnProperty(i))
        {
            o = result[i];
            
            dt = kestava.iso_8601_to_date(o.created_when_formatted);
            
            p = $(document.createElement('div'))
                .append(
                    $(document.createElement('p'))
                        .addClass('ago')
                        .text(kestava.get_fuzzy_time_ago(dt)))
                .append(
                    $(document.createElement('p'))
                        .addClass('timestamp')
                        .text(dt.getTime())
                        .attr('style', 'display:none'))
                .append(
                    $(document.createElement('p'))
                        .text(o.message_text))
                .appendTo(container);
            
            // Use an interval timer to continuously update the displayed
            // timestamp text
            setInterval((function() {
                var a = p;
                return function() {
                    $('.ago', a)
                        .text(kestava.get_fuzzy_time_ago(
                            new Date(parseInt($('.timestamp', a).text()))));
                }
            }()),
            5000);
        }
    }
};