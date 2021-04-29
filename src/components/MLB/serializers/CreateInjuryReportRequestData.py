from serialize_mcr import SerializeMCR


class PlayerModelData(SerializeMCR):
    schema = [
        {'name': 'player_id', 'type': (str, 'uuid')},
        {'name': 'player_name', 'type': (str, )},
        {'name': 'bats', 'type': (str, ('L', 'R', 'S'))},
        {'name': 'throws', 'type': (str, ('L', 'R', 'S'))},
        {'name': 'player_position', 'type': (str, ('C', 'P', '1B', '2B', 'SS', '3B', 'LF', 'CF', 'RF', 'DH', 'IF', 'OF'))},
        {'name': 'team_id', 'type': (str, 'uuid')},
        {'name': 'starter', 'type': (bool, )}
    ]


class CreateInjuryReportRequestData(SerializeMCR):
    schema = [
        {'name': 'players', 'is_compound': True, 'compound_schema': PlayerModelData},
        {'name': 'date', 'type': (str, )}
    ]