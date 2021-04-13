from serialize_mcr import SerializeMCR


class UpdateSeasonRequestData(SerializeMCR):
    schema = [
        {'name': 'sport_id', 'type': (str, 'uuid'), 'optional': True},
        {'name': 'season_start_date', 'type': (str,), 'optional': True},
        {'name': 'season_end_date', 'type': (str,), 'optional': True},
        {'name': 'champion_id', 'type': (str, 'uuid'), 'optional': True},
        {'name': 'runnerup_id', 'type': (str, 'uuid'), 'optional': True}
    ]
