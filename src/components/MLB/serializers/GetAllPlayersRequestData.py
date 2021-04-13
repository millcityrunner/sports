from serialize_mcr import SerializeMCR


class GetAllPlayersRequestData(SerializeMCR):
    schema = [
        {'name': 'player_name', 'type': (str,), 'optional': True},
        {'name': 'bats', 'type': (str, ('R', 'L', 'S')), 'optional': True},
        {'name': 'throws', 'type': (str, ('R', 'L', 'S')), 'optional': True},
        {'name': 'player_position',
         'type': (str, ('P', 'C', '1B', '2B', 'SS', '3B', 'OF', 'IF', 'LF', 'CF', 'RF', 'DH')), 'optional': True},
        {'name': 'starter', 'type': (bool,), 'optional': True}
    ]
