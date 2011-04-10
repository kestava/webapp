// File: public-timeline.js

var kestava;

$(function() {
    // Start loading the public timeline
    // by default, we load the last 50 entries
    kestava.publicTimeline.beginLoadTimeline(50);
});

kestava.publicTimeline = (function() {
    var publicTimelineUrl = sprintf(
            'http://%s/public',
            kestava.timelineServerHostname),
        nextMessagesUrl = sprintf(
            'http://%s/next',
            kestava.timelineServerHostname);
    
    return {
        beginLoadTimeline: function(maxEntries) {
            var url = publicTimelineUrl
                + sprintf('?maxCount=%d&callback=?', maxEntries);
                
            $.getJSON(url, kestava.publicTimeline.endLoadTimeline);
        },

        endLoadTimeline: function(result) {
            var k = kestava,
                i, o, p,
                container = $('#innerContainer'),
                formatName = function(a) {
                    return a ? a : 'System';
                },
                lastId,
                updateTimeAgo = function(a) {
                    return function() {
                        $('.ago', a)
                            .text(k.utilities.getFuzzyTimeAgo(
                                new Date(parseInt($('.timestamp', a).text(), 10))));
                    };
                };
            
            for (i in result) {
                if (result.hasOwnProperty(i)) {
                    o = k.classes.TimelineMessageFromJSON(result[i]);
                    
                    // Save the last message id for later
                    if (!lastId) { lastId = parseInt(o.messageId, 10); }
                    
                    p = $(document.createElement('div'))
                        .addClass('messageContainer')
                        .append(
                            $(document.createElement('p'))
                                .addClass('ago')
                                .text(o.getFuzzyTimeAgo()))
                        .append(
                            $(document.createElement('p'))
                                .addClass('email')
                                .text(formatName(o.email)))
                        .append(
                            $(document.createElement('p'))
                                .addClass('timestamp')
                                .text(o.getTimestamp())
                                .attr('style', 'display:none'))
                        .append(
                            $(document.createElement('p'))
                                .addClass('messageId')
                                .text(o.messageId)
                                .attr('style', 'display:none'))
                        .append(
                            $(document.createElement('p'))
                                .text(o.messageText))
                        .appendTo(container);
                    
                    // Use an interval timer to continuously update the displayed
                    // timestamp text
                    setInterval(
                        updateTimeAgo(p),
                        5000);
                }
            }
            
            // Begin comet request
            k.publicTimeline.beginRequestNextMessage(lastId);
        },
        
        beginRequestNextMessage: function(id) {
            var url = nextMessagesUrl
                + sprintf('?lastId=%d&maxCount=%d&callback=?', id, 10);
                
            $.getJSON(url, kestava.publicTimeline.endRequestNextMessage);
        },
        
        endRequestNextMessage: function(result) {
            var jake = 0;
        }
    };
}());