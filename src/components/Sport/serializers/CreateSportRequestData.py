from serialize_mcr import SerializeMCR


class CreateSportRequestData(SerializeMCR):
    schema = [
        {'name': 'name', 'type': (str, ('MLB', 'NBA', 'NFL', 'NCAAMB', 'NHL', 'ESPORTS'))},
    ]