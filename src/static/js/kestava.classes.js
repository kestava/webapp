var kestava;

kestava.classes = (function() {
    var k = kestava;
    return {
        TimelineMessage: function(o) {
            this.dt = k.utilities.iso8601ToDate(o.created_when_formatted);
            
            this.messageId = parseInt(o.message_id, 10);
            this.messageText = o.message_text;
            this.email = o.email;
            
            this.getTimestamp = function() {
                return this.dt.getTime();
            };
            
            this.getFuzzyTimeAgo = function() {
                return k.utilities.getFuzzyTimeAgo(this.dt);
            };
        }
    }
}());

kestava.classes.TimelineMessageFromJSON = function(o) {
    return new kestava.classes.TimelineMessage(o);
};