from datetime import datetime

from adjax.serializer import serializer, ObjectType

from .models import CustomObject


@serializer.enable
class CustomType(ObjectType):
    name = 'custom'
    cls = CustomObject

    @classmethod
    def encode(cls, value):
        return {
            'x': value.x,
            'y': value.y,
        }

    @classmethod
    def decode(cls, value):
        return CustomObject(value['x'], value['y'])


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
