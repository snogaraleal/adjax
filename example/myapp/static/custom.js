ADJAX.register(function (xhr) {
    xhr.setRequestHeader('X-CSRFToken', adjax.utils.getCookie('csrftoken'));
});

var CustomType = function (x, y) {
    this.x = x;
    this.y = y;
};

CustomType.prototype.getX = function () {
    return this.x;
};

CustomType.prototype.getY = function () {
    return this.y;
};

ADJAX.serializer.register(
    'custom', CustomType, new adjax.Type(function (value) {
        return {
            'x': value.getX(),
            'y': value.getY(),
        };
    }, function (value) {
        return (new CustomType(value['x'], value['y']));
    })
);

Date.prototype.toJSON = undefined;

ADJAX.serializer.register(
    'datetime', Date, new adjax.Type(function (value) {
        return {
            'value': value.toISOString(),
        };
    }, function (value) {
        return new Date(value['value']);
    })
);
