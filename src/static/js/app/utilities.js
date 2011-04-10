var app;

app.utilities = (function() {
    return {
        iso8601ToDate: function(input)
        {
            var regexp = /(\d\d\d\d)(-)?(\d\d)(-)?(\d\d)(T)?(\d\d)(:)?(\d\d)(:)?(\d\d)(\.\d+)?(Z|([+\-])(\d\d)(:)?(\d\d))/,
                o = new Date(),
                d = input.match(new RegExp(regexp)),
                offset = 0;
        
            if (d)
            {
                o.setUTCDate(1);
                o.setUTCFullYear(parseInt(d[1],10));
                o.setUTCMonth(parseInt(d[3],10) - 1);
                o.setUTCDate(parseInt(d[5],10));
                o.setUTCHours(parseInt(d[7],10));
                o.setUTCMinutes(parseInt(d[9],10));
                o.setUTCSeconds(parseInt(d[11],10));
                o.setUTCMilliseconds(0);
                
                if (d[13] !== 'Z')
                {
                    offset = (d[15] * 60) + parseInt(d[17],10);
                    offset *= ((d[14] === '-') ? -1 : 1);
                    o.setTime(this.getTime() - offset * 60 * 1000);
                }
            }
            else
            {
                o.setTime(Date.parse(input));
            }
            return o;
        },
        getFuzzyTimeAgo: function(input)
        {
            var elapsed = (new Date()).getTime() - input.getTime(),
                seconds,
                minutes,
                hours,
                roundingFactor = 5,
                future = 0 > elapsed;
            
            elapsed = Math.abs(elapsed);
            
            // Do as little math as possible.
            // Try not to do any math for items a day or more old.
            if (elapsed < 86400000)
            {
                hours = Math.floor(elapsed / 3600000);
                if (1 > hours)
                {
                    minutes = Math.floor(elapsed / 60000);
                    if (1 > minutes)
                    {
                        seconds =  Math.floor((elapsed / 1000) / roundingFactor) * roundingFactor;
                        if (10 > seconds)
                        {
                            return future ? 'In a few seconds' : 'A few seconds ago';
                        }
                        return future ? 'In ' + seconds + ' seconds' : seconds + ' seconds ago';
                    }
                    else if (1 == minutes)
                    {
                        return future ? 'In 1 minute' : '1 minute ago';
                    }
                    return future ? 'In ' + minutes + ' minutes' : minutes + ' minutes ago';
                }
                else if (1 == hours)
                {
                    return future ? 'In 1 hour' : '1 hour ago';
                }
                return future ? 'In ' + hours + ' hours' : hours + ' hours ago';
            }
            
            return (future ? 'On ' : '')
                + input.getDate()
                + ' '
                + app.utilities.getMonthString(input.getMonth())
                + ' '
                + input.getFullYear();
        },
        getMonthString: function(month)
        {
            var months = [
                { 'name': 'Jan' },
                { 'name': 'Feb' },
                { 'name': 'Mar' },
                { 'name': 'Apr' },
                { 'name': 'May' },
                { 'name': 'Jun' },
                { 'name': 'Jul' },
                { 'name': 'Aug' },
                { 'name': 'Sep' },
                { 'name': 'Oct' },
                { 'name': 'Nov' },
                { 'name': 'Dec' }
            ];
            
            return months[month].name;
        }
    };
}());