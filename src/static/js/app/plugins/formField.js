/*!
 * app/plugins/formField.js
 */
var jQuery, console, document;

(function($) {
    
    var methods = {};
    
    methods.init = function(options) {
        var settings = {};
        
        if (options) {
            $.extend(settings, options);
        }
        
        this.each((function(a) {
            return function() {
                var $t = $(this),
                    data = $t.data('formField');
                    
                if (!data) {
                    $t.data('formField', a);
                }
            };
        }(settings)));
    };
        
    methods.updateImage = function(state, insertAfter) {
        var stateData = this.data('formField').stateData;
        insertAfter = insertAfter ? insertAfter : this;
        if (!stateData.hasOwnProperty(state)) {
            throw 'Invalid state: ' + state;
        }
        this.siblings('.stateImage').remove();
        insertAfter.after($(document.createElement('img'))
            .attr('src', stateData[state].src)
            .attr('alt', stateData[state].alt)
            .addClass('stateImage'));
    };
    
    methods.updateMessage = function(message, insertAfter) {
        insertAfter = insertAfter ? insertAfter : this;
        this.siblings('.fieldMessage').remove();
        insertAfter.after($('<span class="fieldMessage">' + message + '</span>'));
    };
    
    methods.setStateData = function(state, src, alt) {
        var data = this.data('formField');
        if (!data.hasOwnProperty('stateData')) {
            data.stateData = {};
        }
        data.stateData[state] = {
            src: src,
            alt: alt
        };
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
