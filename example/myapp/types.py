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
