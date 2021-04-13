from serialize_mcr import SerializeMCR


class CreateSeasonRequestData(SerializeMCR):
    schema = [
        {'name': 'season_start_date', 'type': (str,)},
        {'name': 'season_end_date', 'type': (str,)},
        {'name': 'champion_id', 'type': (str, 'uuid'), 'optional': True, 'nullable': True},
        {'name': 'runnerup_id', 'type': (str, 'uuid'), 'optional': True, 'nullable': True}
    ]
