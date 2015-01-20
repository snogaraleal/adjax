from django.test import TestCase

from ..serializer import ObjectType, Serializer


class ObjectTypeTestCase(TestCase):

    def test_encode_decode(self):
        """ Test encode and decode methods.
        """

        value = 42
        self.assertEqual(ObjectType.decode(ObjectType.encode(value)), value)


class SerializerTestCase(TestCase):

    def test_init(self):
        """ Test object type registering on initialization.
        """

        class CustomObject(object):
            pass

        class CustomType(ObjectType):
            name = 'custom'
            cls = CustomObject

        serializer = Serializer(object_types=(CustomType,))
        self.assertIn(CustomType, serializer.object_types)

    def test_invalid_enable(self):
        """ Test call to enable custom type without proper attributes.
        """

        class CustomObject(object):
            pass

        class MissingNameObjectType(ObjectType):
            cls = CustomObject

        class MissingClsObjectType(ObjectType):
            name = 'custom'

        serializer = Serializer()

        self.assertRaises(ValueError, serializer.enable,
                          MissingNameObjectType)

        self.assertRaises(ValueError, serializer.enable,
                          MissingClsObjectType)

    def test_valid_enable_disable(self):
        """ Test valid call to enable custom type.
        """

        class CustomObject(object):
            pass

        class ValidObjectType(ObjectType):
            name = 'custom'
            cls = CustomObject

        serializer = Serializer()

        serializer.enable(ValidObjectType)

        self.assertIn(ValidObjectType, serializer.object_types)
        self.assertIn(ValidObjectType.cls, serializer.object_types_by_cls)
        self.assertIn(ValidObjectType.name, serializer.object_types_by_name)

        serializer.disable(ValidObjectType)

        self.assertNotIn(ValidObjectType, serializer.object_types)
        self.assertNotIn(ValidObjectType.cls, serializer.object_types_by_cls)
        self.assertNotIn(ValidObjectType.name,
                         serializer.object_types_by_name)

    def test_encode_decode(self):
        """ Test encode and decode functions.
        """

        class CustomObject(object):
            def __init__(self, value):
                self.value = value

            def __eq__(self, other):
                return self.value == other.value

        class ValidObjectType(ObjectType):
            name = 'custom'
            cls = CustomObject

            @classmethod
            def encode(cls, instance):
                return {
                    'value': instance.value,
                }

            @classmethod
            def decode(cls, data):
                return cls.cls(data['value'])

        serializer = Serializer()
        serializer.enable(ValidObjectType)

        instance = CustomObject(42)

        encoded = serializer.encode({
            'key': instance,
        })

        decoded = serializer.decode(encoded)

        self.assertEqual(decoded['key'], instance)

    def test_invalid_encode(self):
        """ Test that an invalid encode implementation raises an error.
        """

        class CustomObject(object):
            def __init__(self, value):
                self.value = value

            def __eq__(self, other):
                return self.value == other.value

        class ValidObjectType(ObjectType):
            name = 'custom'
            cls = CustomObject

            @classmethod
            def encode(cls, instance):
                return 20

            @classmethod
            def decode(cls, data):
                return cls.cls(data['value'])

        serializer = Serializer()
        serializer.enable(ValidObjectType)

        self.assertRaises(TypeError, serializer.encode, {
            'key': CustomObject(42),
        })
