var adjax = (function () {
    var utils = (function() {
        /*
         * Equivalent to python's zip(...)
         *
         * zip([
         *     ['a', 'b', 'c'],
         *     [1, 2, 3],
         * ])
         *
         * returns [
         *     ['a', 1],
         *     ['b', 2],
         *     ['c', 3],
         * ]
         */
        var zip = function (arrays) {
            return Array.apply(
                null, Array(arrays[0].length)
            ).map(function (_, i) {
                return arrays.map(function (array) {
                    return array[i];
                });
            });
        };

        /*
         * Equivalent to python's dict(...)
         *
         * obj([
         *     ['a', 1],
         *     ['b', 2],
         *     ['c', 3],
         * ])
         *
         * returns {
         *     'a': 1,
         *     'b': 2,
         *     'c': 3,
         * }
         */
        var obj = function (array) {
            var data = {};
            array.forEach(function (item) {
                data[item[0]] = item[1];
            });
            return data;
        };

        /**
         * Get the value of the specified cookie
         */
        var cookie = function (name) {
            var value = '; ' + document.cookie;
            var parts = value.split('; ' + name + '=');
            if (parts.length == 2) {
                return parts.pop().split(';').shift();
            }
        };

        return {
            'zip': zip,
            'obj': obj,
            'cookie': cookie,
        };
    })();

    /**
     * Error
     */
    var Error = function (message) {
        this.message = message;
    };

    Error.prototype.toString = function () {
        return 'ADJAX: ' + this.message;
    };

    /**
     * Custom type
     */
    var Type = function (encode, decode) {
        this.encode = encode;
        this.decode = decode;
    };

    /**
     * Object capable of serializing custom types
     */
    var Serializer = function (type) {
        this.type = type;
        this.types = {};
    };

    Serializer.INTERNAL_TYPE_NAME = '__name__';

    /**
     * Register custom type
     */
    Serializer.prototype.register = function (name, constructor, type) {
        constructor[Serializer.INTERNAL_TYPE_NAME] = name;
        this.types[name] = type;
    };

    /**
     * Encode data to JSON
     */
    Serializer.prototype.encode = function (data) {
        return JSON.stringify(data, (function (key, value) {
            if (key !== '' && value && typeof value === 'object') {
                var name = value.constructor[Serializer.INTERNAL_TYPE_NAME];
                if (name in this.types) {
                    var data = this.types[name].encode(value);
                    data[this.type] = name;
                    return data;
                }
            }
            return value;
        }).bind(this));
    };

    /**
     * Decode data from JSON
     */
    Serializer.prototype.decode = function (data) {
        return JSON.parse(data, (function (key, value) {
            if (value && typeof value === 'object' &&
                    value[this.type] !== undefined) {
                var name = value[this.type];
                if (this.types[name] === undefined) {
                    throw new Error(
                        "Custom type '" + name + "' not implemented");
                }
                return this.types[name].decode(value);
            }
            return value;
        }).bind(this));
    };

    /**
     * Interface object
     */
    var Interface = function (data, views, type) {
        this.serializer = new Serializer(type);
        this.data = data;
        this.views = views;
        this.pipeline = [];
        this.apps = {};

        for (var app in views) {
            this.apps[app] = {};
            for (var name in views[app]) {
                this.apps[app][name] = this.getView(app, name);
            }
        }
    };

    /**
     * Register XHR pipeline function
     */
    Interface.prototype.register = function (func) {
        this.pipeline.push(func);
    };

    /**
     * Create function for calling the specified view
     */
    Interface.prototype.getView = function (app, name) {
        if (this.views[app] === undefined) {
            throw new Error("App '" + app + "' does not exist");
        }

        if (this.views[app][name] === undefined) {
            throw new Error(
                "View '" + name + "' does not exist in app '" + app + "'");
        }

        var view = this.views[app][name];

        return (function () {
            var values = Array.prototype.slice.call(arguments, 0);

            var callback;
            if (typeof values[values.length - 1] === 'function') {
                callback = values.pop();
            }

            var update;
            if (typeof values[values.length - 1] === 'function') {
                update = values.pop();
            }

            var data = utils.obj(utils.zip([view['args'], values]));
            if (update) {
                update(data);
            }

            var self = this;

            var promise = new Promise(function (resolve, reject) {

                var xhr = new XMLHttpRequest();
                xhr.open('POST', view['url']);

                xhr.onreadystatechange = function () {
                    try {
                        if (xhr.readyState === XMLHttpRequest.DONE) {
                            if (xhr.status === 0 && !content) {
                                throw new Error('Connection error');
                            }

                            var content = xhr.responseText;
                            var data = self.serializer.decode(content);
                            if (data && data.error) {
                                throw new Error(data.message);
                            }
                            resolve(data);
                        }
                    } catch (exception) {
                        reject(exception);
                    }
                };

                xhr.onerror = function (event) {
                    reject(event);
                };

                self.pipeline.forEach(function (item) {
                    item(xhr);
                });

                try {
                    xhr.send(self.serializer.encode(data));
                } catch (exception) {
                    reject(exception);
                }
            });

            if (callback) {
                promise.then(callback);
            }

            return promise;
        }).bind(this);
    };

    return {
        'utils': utils,

        'Type': Type,
        'Serializer': Serializer,
        'Interface': Interface,
    }
})();
