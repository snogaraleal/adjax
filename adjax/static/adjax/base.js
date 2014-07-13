(function () {
    'use strict';

    // Get object constructor
    Object.prototype.getType = function () {
        var funcNameRegex = /function (.{1,})\(/;
        var results = (funcNameRegex).exec((this).constructor.toString());
        return (results && results.length > 1) ? results[1] : '';
    };

    // Equivalent to python's zip(...)
    Array.prototype.zip = function () {
        return Array.apply(
            null, [this[0].length]
        ).map(function (_, i) {
            return this.map(function (array) {
                return array[i];
            });
        });
    };

    // Equivalent to python's dict(...)
    Array.prototype.obj = function () {
        var data = {};
        this.forEach(function (item) {
            data[item[0]] = item[1];
        });
        return data;
    };

    /*
     * Cookie manipulation
     */
    var Cookie = {
        // Get the specificated cookie
        get: function (name) {
            var value = '; ' + document.cookie,
                parts = value.split('; ' + name + '=');

            return (parts.length == 2) ? parts.pop().split(';').shift() : null;
        },

        // TODO: Method not implemented
        set: function () { return null; },

        // TODO: Method not implemented
        all: function () { return null; }
    };

    /*
     * Serializer
     */
    var Serializer = {

        // Serialize to string
        encode: function (data) {
            return JSON.stringify(data, function (key, value) {
                if (key !== '' && typeof value === 'object') {
                    var type = value.getType();
                    if (type in funcs) {
                        return funcs[type].encode(value);
                    }
                }
                return value;
            });
        },

        // Deserialize from string
        decode: function (data) {
            return JSON.parse(data, function (key, value) {
                if (typeof value === 'object' && value[type] !== undefined) {
                    return types[value[type]].decode(value);
                }
                return value;
            });
        }
    };

    /*
     * Call AJAX view
     */
    var Adjax = function (data, views, types, type) {
        var funcs = {};
        this.pipeline = [];

        for (var name in types) {
            if (types.hasOwnProperty(name)) {
                // TODO: Replace this evals
                eval('var encode = (' + types[name].encode + ');');
                eval('var decode = (' + types[name].decode + ');');

                types[name].encode = encode;
                types[name].decode = decode;

                funcs[types[name].type] = {
                    'encode': encode,
                    'decode': decode,
                };
            }
        }
    }, adjax = Adjax;

    Adjax.prototype.call = function (app) {
        return function (name) {
            var view = views[app][name];

            return function () {
                var callback,
                    xhr = new XMLHttpRequest(),
                    values = Array.prototype.slice.call(arguments, 0),
                    data = [view.args, values].zip().obj();

                // Get request data and callback
                if (typeof arguments[arguments.length - 1] === 'function') {
                    callback = values.pop();
                }

                // Make request
                xhr.open('POST', view.url);
                if (callback) {
                    xhr.onreadystatechange = function () {
                        if (xhr.readyState === 4) {
                            var data;
                            try {
                                data = Serializer.decode(xhr.responseText);
                            } catch (e) {
                                data = null;
                            }
                            callback(data);
                        }
                    };
                }
                this.pipeline.forEach(function (item) {
                    item(xhr);
                });
                xhr.send(Serializer.encode(data));
            };
        };
    };

}());
