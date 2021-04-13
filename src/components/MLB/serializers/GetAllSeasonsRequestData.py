from serialize_mcr import SerializeMCR


class GetAllSeasonsRequestData(SerializeMCR):
    schema = [
        {'name': 'season_start_date', 'type': (str, ), 'optional': True},
        {'name': 'season_end_date', 'type': (str, ), 'optional': True},
        {'name': 'champion_id', 'type': (str, 'uuid'), 'optional': True},
        {'name': 'runnerup_id', 'type': (str, 'uuid'), 'optional': True}
    ]
