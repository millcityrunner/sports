from utils.exceptions import Error
from utils.create_app import logger

from components.MLB.services import seasons as SeasonService
from components.MLB.services import games as GameService
from components.MLB.services import expectations as ExpectationService
from components.MLB.services import injury_reports as InjuryReportService
from components.MLB.services import weather_reports as WeatherReportService
from components.MLB.services import schedules as ScheduleService
from components.MLB.services import players as PlayerService
from components.MLB.services import teams as TeamService

from components.MLB.serializers.CreateSeasonRequestData import CreateSeasonRequestData
from components.MLB.serializers.UpdateSeasonRequestData import UpdateSeasonRequestData

from components.MLB.serializers.CreateTeamRequestData import CreateTeamRequestData
from components.MLB.serializers.UpdateTeamRequestData import UpdateTeamRequestData

from components.MLB.serializers.CreatePlayerRequestData import CreatePlayerRequestData
from components.MLB.serializers.UpdatePlayerRequestData import UpdatePlayerRequestData


def create_season(request_body, sport_id):
    if not request_body or request_body == '{}':
        logger.error(f'Failed to process the request to create a season. Failed to supply a valid request body, '
                     f'request_body: {request_body}')
        return Error.INVALID_VALUE

    try:
        logger.info(f'Attempted to serialize the request body for creating a season.')
        req_data = CreateSeasonRequestData(data=request_body)

    except (ValueError, KeyError, AttributeError, TypeError) as e:
        logger.error(f'Failed to process the request to create a season. Failed to supply a valid request body, '
                     f'request_body: {request_body}')
        return Error.INVALID_VALUE

    else:
        champion_id = request_body.get('champion_id', None)
        runnerup_id = request_body.get('runnerup_id', None)

        return SeasonService.create_season(sport_id=sport_id,
                                           season_start_date=req_data.season_start_date,
                                           season_end_date=req_data.season_end_date,
                                           champion_id=champion_id,
                                           runnerup_id=runnerup_id)


def get_season_by_id(season_id):
    season_model = SeasonService.get_season_by_id(season_id=season_id)

    if season_model == Error.RESOURCE_NOT_FOUND:
        return Error.RESOURCE_NOT_FOUND

    return season_model


def get_all_seasons(**filters):
    season_models = SeasonService.get_all_seasons(**filters)

    if season_models == Error.EMPTY_SET:
        return Error.EMPTY_SET

    return season_models


def update_season(season_id, request_body):
    if not request_body or request_body == '{}':
        logger.error(f'Failed to process the request to update a season. Failed to supply a valid request body, '
                     f'request_body: {request_body}')
        return Error.INVALID_VALUE

    try:
        logger.info(f'Attempted to serialize the request body for updating a season.')
        req_data = UpdateSeasonRequestData(data=request_body)

    except (ValueError, KeyError, AttributeError, TypeError) as e:
        logger.error(f'Failed to process the request to create a season. Failed to supply a valid request body, '
                     f'error: {e}, request_body: {request_body}')
        return Error.INVALID_VALUE

    sport_id = request_body.get('sport_id', None)
    season_start_date = request_body.get('season_start_date', None)
    season_end_date = request_body.get('season_end_date', None)
    champion_id = request_body.get('champion_id', None)
    runnerup_id = request_body.get('runnerup_id', None)

    season_model = SeasonService.update_season(season_id=season_id,
                                               sport_id=sport_id,
                                               season_start_date=season_start_date,
                                               season_end_date=season_end_date,
                                               champion_id=champion_id,
                                               runnerup_id=runnerup_id)

    if season_model == Error.RESOURCE_NOT_FOUND:
        return Error.RESOURCE_NOT_FOUND

    return season_model


def delete_season(season_id):
    season_model = SeasonService.delete_season(season_id=season_id)

    if season_model == Error.RESOURCE_NOT_FOUND:
        return Error.RESOURCE_NOT_FOUND

    return season_model


def create_team(request_body, season_id):
    if not request_body or request_body == '{}':
        logger.error(f'Failed to process the request to create a team. Failed to supply a valid request body, '
                     f'request_body: {request_body}')
        return Error.INVALID_VALUE

    try:
        logger.info(f'Attempted to serialize the request body for creating a team.')
        req_data = CreateTeamRequestData(data=request_body)

    except (ValueError, KeyError, AttributeError, TypeError) as e:
        logger.error(f'Failed to process the request to create a team. Failed to supply a valid request body, '
                     f'request_body: {request_body}')
        return Error.INVALID_VALUE

    else:
        team_model = TeamService.create_team(team_name=req_data.team_name,
                                             team_city=req_data.team_city,
                                             conference_id=req_data.conference_id,
                                             division_id=req_data.division_id,
                                             season_id=season_id)

    return team_model


def get_team_by_id(team_id):
    team_model = TeamService.get_team_by_id(team_id=team_id)

    if team_model == Error.RESOURCE_NOT_FOUND:
        return Error.RESOURCE_NOT_FOUND

    return team_model


def get_all_teams(**filters):
    team_models = TeamService.get_all_teams(**filters)

    return team_models


def update_team(team_id, request_body):
    if not request_body or request_body == '{}':
        logger.error(f'Failed to process the request to update a team. Failed to supply a valid request body, '
                     f'request_body: {request_body}')
        return Error.INVALID_VALUE

    try:
        logger.info(f'Attempted to serialize the request body for updating a team.')
        req_data = UpdateTeamRequestData(data=request_body)

    except (ValueError, KeyError, AttributeError, TypeError) as e:
        logger.error(f'Failed to process the request to create a team. Failed to supply a valid request body, '
                     f'error: {e}, request_body: {request_body}')
        return Error.INVALID_VALUE

    team_city = request_body.get('team_city', None)
    team_name = request_body.get('team_name', None)
    conference_id = request_body.get('conference_id', None)
    division_id = request_body.get('division_id', None)
    season_id = request_body.get('season_id', None)

    team_model = TeamService.update_team(team_id=team_id,
                                         season_id=season_id,
                                         team_city=team_city,
                                         team_name=team_name,
                                         conference_id=conference_id,
                                         division_id=division_id)

    if team_model == Error.RESOURCE_NOT_FOUND:
        return Error.RESOURCE_NOT_FOUND

    return team_model


def delete_team(team_id):
    team_model = TeamService.delete_team(team_id=team_id)

    if team_model == Error.RESOURCE_NOT_FOUND:
        return Error.RESOURCE_NOT_FOUND

    return team_model


def create_player(request_body, team_id):
    if not request_body or request_body == '{}':
        logger.error(f'Failed to process the request to create a player. Failed to supply a valid request body, '
                     f'request_body: {request_body}')
        return Error.INVALID_VALUE

    try:
        logger.info(f'Attempted to serialize the request body for creating a player.')
        req_data = CreatePlayerRequestData(data=request_body)

    except (ValueError, KeyError, AttributeError, TypeError) as e:
        logger.error(f'Failed to process the request to create a player. Failed to supply a valid request body, '
                     f'request_body: {request_body}')
        return Error.INVALID_VALUE

    else:
        player_model = PlayerService.create_player(player_name=req_data.player_name,
                                                   bats=req_data.bats,
                                                   throws=req_data.throws,
                                                   player_position=req_data.player_position,
                                                   starter=req_data.starter,
                                                   team_id=team_id)

    return player_model


def get_player_by_id(player_id):
    player_model = PlayerService.get_player_by_id(player_id=player_id)

    if player_model == Error.RESOURCE_NOT_FOUND:
        return Error.RESOURCE_NOT_FOUND

    return player_model


def get_all_players(**filters):
    player_models = PlayerService.get_all_players(**filters)

    return player_models


def update_player(request_body, player_id):
    if not request_body or request_body == '{}':
        logger.error(f'Failed to process the request to update a team. Failed to supply a valid request body, '
                     f'request_body: {request_body}')
        return Error.INVALID_VALUE

    try:
        logger.info(f'Attempted to serialize the request body for updating a team.')
        req_data = UpdatePlayerRequestData(data=request_body)

    except (ValueError, KeyError, AttributeError, TypeError) as e:
        logger.error(f'Failed to process the request to create a team. Failed to supply a valid request body, '
                     f'error: {e}, request_body: {request_body}')
        return Error.INVALID_VALUE

    team_id = request_body.get('team_id', None)
    player_name = request_body.get('player_name', None)
    bats = request_body.get('bats', None)
    throws = request_body.get('throws', None)
    player_position = request_body.get('player_position', None)
    starter = request_body.get('starter', None)

    player_model = PlayerService.update_player(player_id=player_id,
                                               team_id=team_id,
                                               player_name=player_name,
                                               bats=bats,
                                               throws=throws,
                                               player_position=player_position,
                                               starter=starter)

    if player_model == Error.RESOURCE_NOT_FOUND:
        return Error.RESOURCE_NOT_FOUND

    return player_model


def delete_player(player_id):
    player_model = PlayerService.delete_player(player_id=player_id)

    if player_model == Error.RESOURCE_NOT_FOUND:
        return Error.RESOURCE_NOT_FOUND

    return player_model

