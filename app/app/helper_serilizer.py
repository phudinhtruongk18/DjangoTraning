from rest_framework import serializers


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)

def inline_serializer(* , fields , data = None, **kwargs):
    serilizer_class = create_serializer_class(name='', fields=fields)
    
    if data is not None:
        return serilizer_class(data, **kwargs)

    return serilizer_class(**kwargs)

