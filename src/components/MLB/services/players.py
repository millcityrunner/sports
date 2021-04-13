from components.MLB.models.players import PlayerModel
from utils.exceptions import Error


def create_player(player_name, bats, throws, player_position, starter, team_id):
    player_model = PlayerModel.create_player(player_name=player_name,
                                             bats=bats,
                                             throws=throws,
                                             player_position=player_position,
                                             starter=starter,
                                             team_id=team_id)

    return player_model


def get_player_by_id(player_id, return_as_model=False):
    player_model = PlayerModel.get_player_by_id(player_id=player_id, return_as_model=return_as_model)

    if player_model is None:
        return Error.RESOURCE_NOT_FOUND

    return player_model


def get_all_players(**filters):
    player_models = PlayerModel.get_all_players(**filters)

    return player_models


def update_player(player_id, team_id, player_name, bats, throws, player_position, starter):
    player_model = PlayerModel.update_player(player_id=player_id,
                                             team_id=team_id,
                                             player_name=player_name,
                                             bats=bats,
                                             throws=throws,
                                             player_position=player_position,
                                             starter=starter)

    return player_model


def delete_player(player_id):
    player_model = PlayerModel.delete_player(player_id=player_id)

    if player_model is None:
        return Error.RESOURCE_NOT_FOUND

    return player_model



