var kestava;

kestava.iso_8601_to_date = function(dString)
{
    var regexp = /(\d\d\d\d)(-)?(\d\d)(-)?(\d\d)(T)?(\d\d)(:)?(\d\d)(:)?(\d\d)(\.\d+)?(Z|([+\-])(\d\d)(:)?(\d\d))/,
        o = new Date(),
        d,
        offset;

    if (dString.toString().match(new RegExp(regexp))) {
        d = dString.match(new RegExp(regexp));
        offset = 0;
        
        o.setUTCDate(1);
        o.setUTCFullYear(parseInt(d[1],10));
        o.setUTCMonth(parseInt(d[3],10) - 1);
        o.setUTCDate(parseInt(d[5],10));
        o.setUTCHours(parseInt(d[7],10));
        o.setUTCMinutes(parseInt(d[9],10));
        o.setUTCSeconds(parseInt(d[11],10));
        if (d[12])
        {
            o.setUTCMilliseconds(parseFloat(d[12]) * 1000);
        }
        else
        {
            o.setUTCMilliseconds(0);
        }
        
        if (d[13] !== 'Z')
        {
            offset = (d[15] * 60) + parseInt(d[17],10);
            offset *= ((d[14] === '-') ? -1 : 1);
            o.setTime(this.getTime() - offset * 60 * 1000);
        }
    }
    else
    {
        o.setTime(Date.parse(dString));
    }
    return o;
};