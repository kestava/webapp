/*!
 * app/plugins/formField.js
 */
var jQuery;

(function($) {
    
    var methods = {
        init: function(options) {
            var settings = {};
            
            if (options) {
                $.extend(settings, options);
            }
            
            this.each(function(a) {
                return function() {
                    var $t = $(this),
                        data = $t.data('formField');
                        
                    if (!data) {
                        $t.data('formField', a);
                    }
                }
            }(settings));
        }
    };
    
    $.fn.formField = function(method) {        
        if (methods[method]) {
            methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        }
        else if (('object' === typeof method) || !method) {
            methods.init.apply(this, arguments);
        }
        else {
            $.error('Method ' + method + ' does not exist on jQuery.formField');
        }
        return this;
    };
}(jQuery));
