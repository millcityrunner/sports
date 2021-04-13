from components.MLB.models.teams import TeamModel
from utils.exceptions import Error


def create_team(team_name, team_city, conference_id, division_id, season_id):
    team_model = TeamModel.create_team(team_name=team_name,
                                       team_city=team_city,
                                       conference_id=conference_id,
                                       division_id=division_id,
                                       season_id=season_id)

    return team_model


def get_team_by_id(team_id):
    team_model = TeamModel.get_team_by_id(team_id=team_id)

    if team_model is not None:
        return team_model

    return Error.RESOURCE_NOT_FOUND


def get_all_teams(**filters):
    team_models = TeamModel.get_all_teams(**filters)

    return team_models


def update_team(team_id, team_name=None, team_city=None, conference_id=None, division_id=None, season_id=None):
    team_model = TeamModel.update_team(team_id=team_id, team_name=team_name, team_city=team_city,
                                       conference_id=conference_id, division_id=division_id,
                                       season_id=season_id)

    if team_model is None:
        return Error.RESOURCE_NOT_FOUND

    return team_model


def delete_team(team_id):
    team_model = TeamModel.delete_team(team_id=team_id)

    if team_model is None:
        return Error.RESOURCE_NOT_FOUND

    return team_model

