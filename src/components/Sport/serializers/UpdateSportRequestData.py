from serialize_mcr import SerializeMCR


class UpdateSportRequestData(SerializeMCR):
    schema = [
        {'name': 'name', 'type': (str, )}
    ]
