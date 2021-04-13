from serialize_mcr import SerializeMCR


class CreateTeamRequestData(SerializeMCR):
    schema = [
        {'name': 'team_name', 'type': (str, )},
        {'name': 'team_city', 'type': (str, )},
        {'name': 'conference_id', 'type': (str, 'uuid')},
        {'name': 'division_id', 'type': (str, 'uuid')}
    ]
