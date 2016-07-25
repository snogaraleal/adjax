# Django ADJAX

**Adjax** lets you call Python functions from JavaScript. Adjax is a simple AJAX-based RPC mechanism for Django that provides argument type validation and an extensible JSON serializer that allows you to plug in your own types.

## Installation

This project supports both **Python 2** and **Python 3**.

Install with `pip install django-adjax`.

## Configuration

### 1. Update settings

Add `adjax` to `INSTALLED_APPS` in your settings file.

Add `adjax.middleware.CsrfEnforceMiddleware` to `MIDDLEWARE_CLASSES`.

Add `adjax.middleware.DispatchErrorMiddleware` to `MIDDLEWARE_CLASSES`.

The `DispatchErrorMiddleware` middleware handles `adjax.views.DispatchError` 
exceptions and returns an error message rather than throwing a 500 server
error. You can replace this middleware with your own.

### 2. Add URLs

Add Adjax URLs to your main URL patterns.

```python
from django.conf.urls import url, include


urlpatterns = [
    # ... your URLs ..

    url(r'^adjax/', include('adjax.urls')),
]
```

### 3. Add JS scripts

Adjax requires 2 JS files to be loaded. The base JS library found in
`static/adjax/base.js` and the interface JS view. Both files can be included
with the `{% adjax_scripts %}` template tag.

```html
{% load adjax %}

<body>
  ...

  <!-- Include Adjax scripts -->
  {% adjax_scripts %}
</body>
```

### 4. Include CSRF token in XHR calls

You need to do this if you are using the CSRF middleware. This code has to be
loaded after `{% adjax_scripts %}`.

```javascript
ADJAX.register(function (xhr) {
    xhr.setRequestHeader('X-CSRFToken', adjax.utils.cookie('csrftoken'));
});
```

## Views (RPC functions)

Adjax looks for RPC functions in the `ajax` module in each app. RPC functions
have to be explicitly exposed with the `@registry.register` decorator. Create
an `ajax.py` file in your app and register the view with the
`@registry.register` decorator.

```python
from adjax.registry import registry

@registry.register
def func1(request, a, b, c=1):
    return {
        # ...
    }
```

You can optionally add type validation to your RPC function with the `@typed`
decorator. This feature uses
[PEP-3107](https://www.python.org/dev/peps/pep-3107/) function annotations.

```python
# myapp/ajax.py

from adjax.registry import registry
from adjax.utils.types import typed

@registry.register
@typed(strict=False)
def do_stuff(request, a: int, b: float, c=1) -> dict:
    return {
        'a': a,
        'b': b,
        'c': c,
    }
```

Since Python 2 doesn't support function annotations you can pass a dictionary of types to the `typed` decorator.

```python
# myapp/ajax.py

from adjax.registry import registry
from adjax.utils.types import typed

@registry.register
@typed({'a': int, 'b': float, 'return': dict}, strict=False)
def do_stuff(request, a, b, c=1):
    return {
        'a': a,
        'b': b,
        'c': c,
    }
```

You can now call this function from JS.

```javascript
ADJAX.apps.myapp.do_stuff(a, b, function (data) {
    console.log(data);
});
```

## Serializer types

Custom serializer types allow you to send and receive objects that are not of a built-in type. Here is a demonstration implementing the date type.

### 1. Server-side serialization

Register a new `ObjectType` with name `datetime`.

```python
from datetime import datetime

from adjax.serializer import serializer, ObjectType


@serializer.enable
class DateTime(ObjectType):
    name = 'datetime'
    cls = datetime

    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

    @classmethod
    def encode(cls, value):
        return {
            'value': value.strftime(cls.DATETIME_FORMAT),
        }

    @classmethod
    def decode(cls, value):
        return datetime.strptime(value['value'], cls.DATETIME_FORMAT)
```

### 2. Client-side serialization

Register a new serializer with the same name as the server-side
implementation which is `datetime`.

```javascript
// Disable implicit serialization in JSON.stringify
Date.prototype.toJSON = undefined;

// For more information see https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify#toJSON_behavior

ADJAX.serializer.register(
    'datetime', Date, new adjax.Type(function (value) {
        return {
            'value': value.toISOString(),
        };
    }, function (value) {
        return new Date(value['value']);
    })
);
```

Now you can send and receive `Date` objects from Python to JS and vice-versa.

## License

This project is under the terms of the MIT license. See LICENSE.
