from serialize_mcr import SerializeMCR


class GetAllSportsRequestData(SerializeMCR):
    schema = [
        {'name': 'name', 'type': (str, ), 'optional': True}
    ]
