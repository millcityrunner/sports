from serialize_mcr import SerializeMCR


class GetAllTeamsRequestData(SerializeMCR):
    schema = [
        {'name': 'team_name', 'type': (str, ), 'optional': True},
        {'name': 'team_city', 'type': (str, ), 'optional': True},
        {'name': 'conference_id', 'type': (str, 'uuid'), 'optional': True},
        {'name': 'division_id', 'type': (str, 'uuid'), 'optional': True},
        {'name': 'season_id', 'type': (str, 'uuid'), 'optional': True}
    ]