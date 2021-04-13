from serialize_mcr import SerializeMCR


class CreatePlayerRequestData(SerializeMCR):
    schema = [
        {'name': 'player_name', 'type': (str,)},
        {'name': 'bats', 'type': (str, ('R', 'L', 'S'))},
        {'name': 'throws', 'type': (str, ('R', 'L', 'S'))},
        {'name': 'player_position',
         'type': (str, ('P', 'C', '1B', '2B', 'SS', '3B', 'OF', 'IF', 'LF', 'CF', 'RF', 'DH'))},
        {'name': 'starter', 'type': (bool,)}
    ]
