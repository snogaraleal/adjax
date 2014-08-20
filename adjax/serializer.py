from json import loads, dumps


class ObjectType(object):
    """ Class defining a pluggable type.
    """

    TYPE = '__type__'

    name = None
    cls = None

    @classmethod
    def encode(cls, value):
        """ Convert value to dictionary.
        """
        return {
            'value': value,
        }

    @classmethod
    def decode(cls, value):
        """ Convert dictionary to value.
        """
        return value['value']


class Serializer(object):
    """ Class for all serialization operations.
    """

    def __init__(self, object_types=None):
        """ Initialize serializer with provided object types list.
        """
        if object_types is None:
            object_types = []

        self.object_types = list(object_types)
        self.object_types_by_cls = {}
        self.object_types_by_name = {}

        for object_type in object_types:
            self.enable(object_type)

    def enable(self, object_type):
        """ Enable the specified object type derived class.
        """

        if object_type.cls is None:
            raise ValueError('Custom type cls must be set')

        if object_type.name is None:
            raise ValueError('Custom type name must be set')

        self.object_types.append(object_type)
        self.object_types_by_cls[object_type.cls] = object_type
        self.object_types_by_name[object_type.name] = object_type

        return object_type

    def disable(self, object_type):
        """ Disable the specified object type derived class.
        """
        self.object_types.remove(object_type)
        self.object_types_by_cls.pop(object_type.cls)
        self.object_types_by_name.pop(object_type.name)

        return object_type

    def encode(self, data):
        """ Serialize data to string.
        """

        def default(value):
            """ Use object type encode if the value is of a registered type.
            """
            object_type = self.object_types_by_cls.get(type(value))

            if object_type:
                value = object_type.encode(value)
                if type(value) != dict:
                    raise TypeError('Object type encode must return dict')
                value[ObjectType.TYPE] = object_type.name

            return value

        return dumps(data, default=default)

    def decode(self, data):
        """ Deserialize data to object.
        """

        def object_hook(dct):
            """ Use object type decode if the dictionary specifies a type.
            """
            if ObjectType.TYPE in dct:
                name = dct[ObjectType.TYPE]

                object_type = self.object_types_by_name.get(name)
                if object_type:
                    return object_type.decode(dct)

            return dct

        return loads(data, object_hook=object_hook)


serializer = Serializer()
