from utils.create_app import app, logger
from utils.error_responses import get_compt_error_response

from components.Sport.serializers import CreatePlayerRequestData
from components.Sport.serializers import CreateTeamRequestData
from components.Sport.serializers import CreateSeasonRequestData


from services import player_service as PlayerService

from urllib import parse

import json

from flask import Response, request, render_template

from src.components.NCAAMB.models.games import GameModel
from models.seasons import SeasonModel
from models.teams import TeamModel
from models.schedules import ScheduleModel

from resources import SeasonModelSerializer, UpdateSeasonModelSerializer, TeamModelSerializer, \
    UpdateTeamModelSerializer, MatchupHistorySerializer, CrawlGamesSerializer, CrawlSchedulesSerializer, \
    AccuracyTrackerSerializer

from services import crawler_service as CrawlerService
from services import matchup_service as MatchupService
from services import seasons as SeasonService
from services import teams as TeamService
from services import schedules as ScheduleService
from services import expectations as ExpectationService
from services import accuracy_tracker as AccuracyTrackerService
from services import home_template_service as HomeTemplateService
from services import golden_weights as GoldenWeightsService
from services import applied_golden_weights_output as AppliedGoldenWeightsOutputService

from utils.create_app import my_app
from utils.database import db
from utils.decorators import door_staff
from utils.exceptions import Error, Exception


##################################################
###################   GENERIC   ##################
##################################################
@app.route('/')
def get_all_available_endpoints():
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)

    return Response(response=json.dumps(sorted(output)),
                    status=200,
                    mimetype='application/json')


##################################################
###################  SEASONS  ####################
##################################################
@app.route('/seasons')
def get_all_seasons():
    filters = request.args

    season_models = SeasonService.get_all_seasons(**filters)

    error = get_compt_error_response(season_models)

    if error is not None:
        return error

    else:
        return Response(response=json.dumps({"all_season_models": season_models}),
                        status=200,
                        mimetype='application/json')


@app.route('/seasons', method=['POST'])
def create_season():
    if not request.get_data().decode() or request.get_data().decode() == '{}':
        logger.error(f'Failed to pass in a request body. request_body: {request.get_data().decode()}')
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    try:
        req_data = CreateSeasonRequestData(data=request.get_json())

    except (AttributeError, ValueError, TypeError, KeyError) as e:
        logger.error(f'Failed to pass in a request body. request_body: {request.get_data().decode()}, error: {e}')
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    season_model = SeasonService.create_season(**req_data.as_dict())

    error = get_compt_error_response(season_model)

    if error is not None:
        return error

    else:
        return Response(response=json.dumps(season_model),
                        status=200,
                        mimetype='application/json')


##################################################
####################  TEAMS   ####################
##################################################
@app.route('/teams')
def get_all_teams():
    filters = request.args

    team_models = TeamService.get_all_teams(**filters)

    error = get_compt_error_response(team_models)

    if error is not None:
        return error

    else:
        return Response(response=json.dumps({'all_team_models': team_models}),
                        status=200,
                        mimetype='application/json')


@app.route('/teams', method=['POST'])
def create_team():
    if not request.get_data().decode() or request.get_data().decode() == '{}':
        logger.error(f'Failed to pass in a request body. request_body: {request.get_data().decode()}')
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    try:
        req_data = CreateTeamRequestData(data=request.get_json())

    except (AttributeError, ValueError, TypeError, KeyError) as e:
        logger.error(f'Failed to pass in a request body. request_body: {request.get_data().decode()}, error: {e}')
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    team_model = TeamService.create_team(**req_data.as_dict())

    error = get_compt_error_response(team_model)

    if error is not None:
        return error

    else:
        return Response(response=json.dumps(team_model),
                        status=200,
                        mimetype='application/json')


##################################################
###################   PLAYERS   ##################
##################################################
@app.route('/players')
def get_all_players():
    filters = request.args

    player_models = PlayerService.get_all_players(**filters)

    error = get_compt_error_response(player_models)

    if error is not None:
        return error

    else:
        return Response(response=json.dumps({'all_player_models': player_models}),
                        status=200,
                        mimetype='application/json')


@app.route('/players', methods=['POST'])
def create_player():
    if not request.get_data().decode() or request.get_data().decode() == '{}':
        logger.error(f'Failed to pass in a request body. request_body: {request.get_data().decode()}')
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    try:
        req_data = CreatePlayerRequestData(data=request.get_json())

    except (AttributeError, ValueError, TypeError, KeyError) as e:
        logger.error(f'Failed to pass in a request body. request_body: {request.get_data().decode()}, error: {e}')
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    player_model = PlayerService.create_player(**req_data.as_dict(), team_id=team_id)

    error = get_compt_error_response(player_model)

    if error is not None:
        return error

    else:
        return Response(response=json.dumps(player_model),
                        status=200,
                        mimetype='application/json')

@my_app.route('/NCAA/MB/initialize_database')
@door_staff
def create_all_tables():
    db.drop_all()
    db.create_all()
    SeasonModel.add_season_baseline()
    TeamModel.add_team_baseline()
    GameModel.add_game_baseline()
    ScheduleModel.add_schedule_baseline()

    response_body = {
        'tables': 'created'
    }

    return Response(json.dumps(response_body), 200, mimetype='application/json')


@my_app.route('/NCAA/MB/seasons', methods=['POST'])
@door_staff
def create_a_season():
    if request.get_data().decode() == '{}' or not request.get_data().decode():
        return Response(response=Exception.invalid_value(property_name='request_body',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    try:
        req_data = SeasonModelSerializer(data=request.get_json())

    except ValueError:
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=eval(request.get_data().decode())),
                        status=400,
                        mimetype='application/json')

    season_model = SeasonService.create_a_season(season_year_start=req_data.season_year_start,
                                                 season_year_end=req_data.season_year_end,
                                                 season_ncaa_champion=req_data.season_ncaa_champion,
                                                 season_ncaa_runnerup=req_data.season_ncaa_runnerup)

    if season_model == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=req_data),
                        status=400,
                        mimetype='application/json')

    else:
        return Response(response=json.dumps(season_model),
                        status=201,
                        mimetype='application/json')


@my_app.route('/NCAA/MB/seasons/<season_id>')
@door_staff
def get_season_by_id(season_id):
    try:
        season_id = int(season_id)

    except (TypeError, ValueError) as e:
        return Response(response=Exception.invalid_value(property_name='season_id',
                                                         value=season_id,
                                                         message=f'`{season_id}` is not integer castable, '
                                                                 f'error: {e}'),
                        status=400,
                        mimetype='application/json')

    season_model = SeasonService.get_season_by_id(season_id=season_id)

    if season_model == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='season_id',
                                                         value=season_id),
                        status=400,
                        mimetype='application/json')

    elif season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    else:
        return Response(response=json.dumps(season_model),
                        status=200,
                        mimetype='application/json')


@my_app.route('/NCAA/MB/seasons/<season_id>', methods=['PUT'])
@door_staff
def update_a_season(season_id):
    try:
        season_id = int(season_id)

    except (TypeError, ValueError) as e:
        return Response(response=Exception.invalid_value(property_name='season_id',
                                                         value=season_id,
                                                         message=f'`{season_id}` is not integer castable, '
                                                                 f'error: {e}'),
                        status=400,
                        mimetype='application/json')

    if request.get_data().decode() == '{}' or not request.get_data().decode():
        return Response(response=Exception.invalid_value(property_name='request_body',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    season_model = SeasonService.get_season_by_id(season_id)

    if season_model == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='season_id',
                                                         value=season_id),
                        status=400,
                        mimetype='application/json')

    elif season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    try:
        req_data = UpdateSeasonModelSerializer(data=request.get_json())

    except ValueError:
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=eval(request.get_data().decode())),
                        status=400,
                        mimetype='application/json')

    season_model = SeasonService.update_a_season(season_id=season_id,
                                                 season_year_start=req_data.season_year_start,
                                                 season_year_end=req_data.season_year_end,
                                                 season_ncaa_champion=req_data.season_ncaa_champion,
                                                 season_ncaa_runnerup=req_data.season_ncaa_runnerup)

    if season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    else:
        return Response(response=json.dumps(season_model),
                        status=202,
                        mimetype='application/json')


@my_app.route('/NCAA/MB/seasons/<season_id>', methods=['DELETE'])
@door_staff
def delete_a_season(season_id):
    try:
        season_id = int(season_id)

    except (TypeError, ValueError) as e:
        return Response(response=Exception.invalid_value(property_name='season_id',
                                                         value=season_id,
                                                         message=f'`{season_id}` is not integer castable, '
                                                                 f'error: {e}'),
                        status=400,
                        mimetype='application/json')

    season_model = SeasonService.get_season_by_id(season_id)

    if season_model == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='season_id',
                                                         value=season_id),
                        status=400,
                        mimetype='application/json')

    elif season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    season_model = SeasonService.delete_a_season(season_id=season_id)

    if season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    elif season_model == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='season_id',
                                                         value=season_id),
                        status=400,
                        mimetype='application/json')

    else:
        return Response(response=json.dumps(season_model),
                        status=202,
                        mimetype='application/json')


@my_app.route('/NCAA/MB/seasons/<season_id>/teams', methods=['POST'])
@door_staff
def create_a_team(season_id):
    try:
        season_id = int(season_id)

    except (TypeError, ValueError) as e:
        return Response(response=Exception.invalid_value(property_name='season_id',
                                                         value=season_id,
                                                         message=f'`{season_id}` is not integer '
                                                                 f'castable, error: {e}'),
                        status=400,
                        mimetype='application/json')

    if request.get_data().decode() == '{}' or not request.get_data().decode():
        return Response(response=Exception.invalid_value(property_name='request_body',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    season_model = SeasonService.get_season_by_id(season_id)

    if season_model == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='season_id',
                                                         value=season_id),
                        status=400,
                        mimetype='application/json')

    elif season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    try:
        req_data = TeamModelSerializer(data=request.get_json())

        # since there are optional params, need to use in addition to req_data
        request_data = eval(request.get_data().decode())
        team_mascot = request_data.get('team_mascot', None)
        team_abbr = request_data.get('team_abbr', None)
        conference = request_data.get('conference', None)

    except ValueError:
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=eval(request.get_data().decode())),
                        status=400,
                        mimetype='application/json')

    team_model = TeamService.create_a_team(team_city=req_data.team_city,
                                           team_mascot=team_mascot,
                                           team_abbr=team_abbr,
                                           conference=conference,
                                           season_id=req_data.season_id)

    if team_model == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='team_city',
                                                         value=req_data.team_city),
                        status=400,
                        mimetype='application/json')

    else:
        body = {
            'team_model': team_model
        }
        return Response(response=json.dumps(body),
                        status=201,
                        mimetype='application/json')


@my_app.route('/NCAA/MB/seasons/<season_id>/teams/<team_id>')
@door_staff
def get_team_by_id(season_id, team_id):
    try:
        season_id = int(season_id)
        team_id = int(team_id)

    except (TypeError, ValueError) as e:
        return Response(response=Exception.invalid_value(property_name=['season_id', 'team_id'],
                                                         value=[season_id, team_id],
                                                         message=f'`{season_id}` or `{team_id}` is not integer '
                                                                 f'castable, error: {e}'),
                        status=400,
                        mimetype='application/json')

    team_model = TeamService.get_team_by_id(team_id=team_id, season_id=season_id)

    if team_model == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name=['season_id', 'team_id'],
                                                         value=[season_id, team_id]),
                        status=400,
                        mimetype='application/json')

    elif team_model == Error.RESOURCE_NOT_FOUND:
        msg = f'the team_id either does not exist, or it does not belong to the specified season_id. ' \
            f'team_id: {team_id}, season_id: {season_id}.'
        return Response(response=Exception.resource_not_found(property_name=['season_id', 'team_id'],
                                                              value=[season_id, team_id],
                                                              message=msg),
                        status=404,
                        mimetype='application/json')

    else:
        return Response(response=json.dumps(team_model),
                        status=200,
                        mimetype='application/json')


@my_app.route('/NCAA/MB/seasons/<season_id>/teams/<team_id>', methods=['PUT'])
@door_staff
def update_a_team(season_id, team_id):
    try:
        season_id = int(season_id)
        team_id = int(team_id)

    except (TypeError, ValueError) as e:
        return Response(response=Exception.invalid_value(property_name=['season_id', 'team_id'],
                                                         value=[season_id, team_id],
                                                         message=f'`{season_id}` or `{team_id}` is not integer '
                                                                 f'castable, error: {e}'),
                        status=400,
                        mimetype='application/json')

    if request.get_data().decode() == '{}' or not request.get_data().decode():
        return Response(response=Exception.invalid_value(property_name='request_body',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    team_model = TeamService.get_team_by_id(season_id, team_id)

    if team_model == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name=['season_id', 'team_id'],
                                                         value=[season_id, team_id]),
                        status=400,
                        mimetype='application/json')

    elif team_model == Error.RESOURCE_NOT_FOUND:
        msg = f'the team_id either does not exist, or it does not belong to the specified season_id. ' \
            f'team_id: {team_id}, season_id: {season_id}.'
        return Response(response=Exception.resource_not_found(property_name=['season_id', 'team_id'],
                                                              value=[season_id, team_id],
                                                              message=msg),
                        status=404,
                        mimetype='application/json')

    try:
        req_data = UpdateTeamModelSerializer(data=request.get_json())

        # since there are optional params, need to use in addition to req_data
        request_data = eval(request.get_data().decode())
        team_city = request_data.get('team_city', None)
        team_mascot = request_data.get('team_mascot', None)
        team_abbr = request_data.get('team_abbr', None)
        conference = request_data.get('conference', None)

    except ValueError:
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=eval(request.get_data().decode())),
                        status=400,
                        mimetype='application/json')

    team_model = TeamService.update_a_team(team_id=team_id,
                                           team_city=team_city,
                                           team_mascot=team_mascot,
                                           team_abbr=team_abbr,
                                           conference=conference,
                                           season_id=season_id)

    if team_model == Error.RESOURCE_NOT_FOUND:
        msg = f'the team_id either does not exist, or it does not belong to the specified season_id. ' \
            f'team_id: {team_id}, season_id: {season_id}.'
        return Response(response=Exception.resource_not_found(property_name=['season_id', 'team_id'],
                                                              value=[season_id, team_id],
                                                              message=msg),
                        status=404,
                        mimetype='application/json')

    else:
        return Response(response=json.dumps(team_model),
                        status=202,
                        mimetype='application/json')


@my_app.route('/NCAA/MB/seasons/<season_id>/teams/<team_id>', methods=['DELETE'])
@door_staff
def delete_a_team(season_id, team_id):
    try:
        season_id = int(season_id)
        team_id = int(team_id)

    except (TypeError, ValueError) as e:
        return Response(response=Exception.invalid_value(property_name=['season_id', 'team_id'],
                                                         value=[season_id, team_id],
                                                         message=f'`{season_id}` or `{team_id}` is not integer '
                                                         f'castable, error: {e}'),
                        status=400,
                        mimetype='application/json')

    team_model = TeamService.get_team_by_id(team_id=team_id, season_id=season_id)

    if team_model == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name=['season_id', 'team_id'],
                                                         value=[season_id, team_id]),
                        status=400,
                        mimetype='application/json')

    elif team_model == Error.RESOURCE_NOT_FOUND:
        msg = f'the team_id either does not exist, or it does not belong to the specified season_id. ' \
            f'team_id: {team_id}, season_id: {season_id}.'
        return Response(response=Exception.resource_not_found(property_name=['season_id', 'team_id'],
                                                              value=[season_id, team_id],
                                                              message=msg),
                        status=404,
                        mimetype='application/json')

    team_model = TeamService.delete_a_team(team_id=team_id, season_id=season_id)

    if team_model == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name=['season_id', 'team_id'],
                                                         value=[season_id, team_id]),
                        status=400,
                        mimetype='application/json')

    elif team_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='team_id',
                                                              value=team_id),
                        status=404,
                        mimetype='application/json')

    else:
        return Response(response=json.dumps(team_model),
                        status=202,
                        mimetype='application/json')


@my_app.route('/NCAA/MB/schedules')
@door_staff
def get_all_schedules():
    all_schedules = ScheduleService.get_all_schedules()

    if all_schedules == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='schedule models',
                                                              value=[]),
                        status=404,
                        mimetype='application/json')

    else:
        return Response(response=json.dumps(all_schedules),
                        status=200,
                        mimetype='application/json')


@my_app.route('/NCAA/MB/matchup_history')
@door_staff
def get_matchup_history():
    if request.get_data().decode() == '{}' or not request.get_data().decode():
        return Response(response=Exception.invalid_value(property_name='request_body',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    try:
        req_data = MatchupHistorySerializer(data=request.get_json())

    except ValueError:
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=eval(request.get_data().decode())),
                        status=400,
                        mimetype='application/json')

    all_matchups = MatchupService.grab_past_matchup_history(team_1_id=req_data.team_1_id, team_2_id=req_data.team_2_id)

    if all_matchups == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    elif all_matchups == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name=['team_1_id', 'team_2_id'],
                                                              value=[req_data.team_1_id, req_data.team_2_id]),
                        status=404,
                        mimetype='application/json')

    else:
        return Response(response=json.dumps(all_matchups),
                        status=200,
                        mimetype='application/json')


@my_app.route('/NCAA/MB/crawl_schedules')
@door_staff
def crawl_schedules():
    if request.get_data().decode() == '{}' or not request.get_data().decode():
        return Response(response=Exception.invalid_value(property_name='request_body',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    try:
        req_data = CrawlSchedulesSerializer(data=request.get_json())

    except ValueError:
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=eval(request.get_data().decode())),
                        status=400,
                        mimetype='application/json')

    all_schedule_models = ScheduleService.get_all_schedules()
    if all_schedule_models == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='all_schedule_models',
                                                              value=[]),
                        status=404,
                        mimetype='application/json')

    else:
        for schedule_model in all_schedule_models:
            away_team_id = schedule_model.get('away_team_id', None)
            home_team_id = schedule_model.get('home_team_id', None)
            start_time = schedule_model.get('start_time', None)
            date = schedule_model.get('date', None)
            over_under_prediction = schedule_model.get('over_under_prediction', None)
            spread_prediction = schedule_model.get('spread_prediction', None)
            winner_prediction = schedule_model.get('winner_prediction', None)
            away_team_score_prediction = schedule_model.get('away_team_score_prediction', None)
            home_team_score_prediction = schedule_model.get('home_team_score_prediction', None)
            away_team_pred_weights_type = schedule_model.get('away_team_pred_weights_type', None)
            home_team_pred_weights_type = schedule_model.get('home_team_pred_weights_type', None)

            expectation_model = ExpectationService.\
                create_an_expectation(away_team_id=away_team_id,
                                      home_team_id=home_team_id,
                                      start_time=start_time,
                                      date=date,
                                      over_under_prediction=over_under_prediction,
                                      spread_prediction=spread_prediction,
                                      winner_prediction=winner_prediction,
                                      away_team_score_prediction=away_team_score_prediction,
                                      home_team_score_prediction=home_team_score_prediction,
                                      away_team_pred_weights_type=away_team_pred_weights_type,
                                      home_team_pred_weights_type=home_team_pred_weights_type)

            if expectation_model == Error.INVALID_VALUE:
                return Response(response=Exception.invalid_value(property_name='[away_team_id, home_team_id, '
                                                                               'start_time, date, '
                                                                               'over_under_prediction, '
                                                                               'spread_prediction, winner_prediction, '
                                                                               'away_team_score_prediction, '
                                                                               'home_team_score_prediction, '
                                                                               'away_team_pred_weights_type, '
                                                                               'home_team_pred_weights_type]',
                                                                 value=[away_team_id, home_team_id, start_time, date,
                                                                        over_under_prediction, spread_prediction,
                                                                        winner_prediction, away_team_score_prediction,
                                                                        home_team_score_prediction,
                                                                        away_team_pred_weights_type,
                                                                        home_team_pred_weights_type]),
                                status=400,
                                mimetype='application/json')

            deleted_schedule_model = ScheduleService.delete_a_schedule(schedule_id=schedule_model.get('schedule_id', None))
            if deleted_schedule_model == Error.RESOURCE_NOT_FOUND:
                return Response(response=Exception.resource_not_found(property_name='schedule_id',
                                                                      value=schedule_model.get('schedule_id', None),
                                                                      message="failed to delete a schedule by id, "
                                                                              f"{schedule_model.get('schedule_id', None)}"),
                                status=404,
                                mimetype='application/json')

            elif deleted_schedule_model == Error.INVALID_VALUE:
                return Response(response=Exception.invalid_value(property_name='schedule_id',
                                                                 value=schedule_model.get('schedule_id', None),
                                                                 message=f"failed to delete a schedule by id, "
                                                                         f"{schedule_model.get('schedule_id', None)}"),
                                status=404,
                                mimetype='application/json')

    web_driver = CrawlerService.startup_automated_browser()

    if web_driver == Error.KEY_ERROR:
        return Response(response=Exception.key_error(property_name='CHROME_DRIVER_PATH',
                                                     value=''),
                        status=503,
                        mimetype='application/json')

    crawler_response = CrawlerService.gather_schedule_on_a_date(driver=web_driver,
                                                                year=req_data.year,
                                                                month=req_data.month,
                                                                day=req_data.day)

    if crawler_response == Error.SECRET_NOT_FOUND:
        return Response(response=Exception.secret_not_found(),
                        status=404,
                        mimetype='application/json')

    elif crawler_response == Error.PAGE_ELEMENT_NOT_FOUND:
        return Response(response=Exception.page_element_not_found(),
                        status=404,
                        mimetype='application/json')

    elif crawler_response == Error.SHUTDOWN_AUTOMATED_BROWSER:
        return Response(response=Exception.shutdown_automated_browser(),
                        status=503,
                        mimetype='application/json')

    elif crawler_response == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='unknown',
                                                         value='',
                                                         message='failed to provide all of the values to the '
                                                                 'find_element_on_page in the '
                                                                 'CrawlService.gather_all_schedules_on_a_date.'),
                        status=400,
                        mimetype='application/json')

    elif crawler_response == Error.FAILED_TO_STARTUP_AUTOMATED_DRIVER:
        return Response(response=Exception.startup_automated_browser(),
                        status=503,
                        mimetype='application/json')

    else:
        return Response(response=json.dumps(crawler_response),
                        status=200,
                        mimetype='application/json')


@my_app.route('/NCAA/MB/crawl_games')
@door_staff
def crawl_games():
    if request.get_data().decode() == '{}' or not request.get_data().decode():
        return Response(response=Exception.invalid_value(property_name='request_body',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    try:
        req_data = CrawlGamesSerializer(data=request.get_json())

    except ValueError:
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=eval(request.get_data().decode())),
                        status=400,
                        mimetype='application/json')

    web_driver = CrawlerService.startup_automated_browser()

    if web_driver == Error.KEY_ERROR:
        return Response(response=Exception.key_error(property_name='CHROME_DRIVER_PATH',
                                                     value=''),
                        status=503,
                        mimetype='application/json')

    crawler_response = CrawlerService.gather_all_scores_on_a_date(driver=web_driver,
                                                                  year=req_data.year,
                                                                  month=req_data.month,
                                                                  day=req_data.day)

    if crawler_response == Error.SECRET_NOT_FOUND:
        return Response(response=Exception.secret_not_found(),
                        status=404,
                        mimetype='application/json')

    elif crawler_response == Error.PAGE_ELEMENT_NOT_FOUND:
        return Response(response=Exception.page_element_not_found(),
                        status=404,
                        mimetype='application/json')

    elif crawler_response == Error.SHUTDOWN_AUTOMATED_BROWSER:
        return Response(response=Exception.shutdown_automated_browser(),
                        status=503,
                        mimetype='application/json')

    elif crawler_response == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='unknown',
                                                         value='',
                                                         message='failed to provide all of the values to the '
                                                                 'find_element_on_page in the '
                                                                 'CrawlService.gather_all_scores_on_a_date.'),
                        status=400,
                        mimetype='application/json')

    elif crawler_response == Error.FAILED_TO_STARTUP_AUTOMATED_DRIVER:
        return Response(response=Exception.startup_automated_browser(),
                        status=503,
                        mimetype='application/json')

    else:
        return Response(response=json.dumps(crawler_response),
                        status=200,
                        mimetype='application/json')


@my_app.route('/NCAA/MB/accuracy_tracker')
@door_staff
def determine_a_dates_accuracy_tracker():
    if request.get_data().decode() == '{}' or not request.get_data().decode():
        return Response(response=Exception.invalid_value(property_name='request_body',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    try:
        req_data = AccuracyTrackerSerializer(data=request.get_json())

    except ValueError:
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=eval(request.get_data().decode())),
                        status=400,
                        mimetype='application/json')

    accuracy_trackers = AccuracyTrackerService.retrieve_accuracy_trackers_on_a_given_date(req_data.date)

    if accuracy_trackers == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='date',
                                                         value=req_data.date),
                        status=400,
                        mimetype='application/json')

    elif accuracy_trackers == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='date',
                                                              value=req_data.date),
                        status=404,
                        mimetype='application/json')

    else:
        return Response(response=json.dumps(accuracy_trackers),
                        status=200,
                        mimetype='application/json')


@my_app.route('/NCAA/MB/golden_weights')
@door_staff
def get_all_golden_weights():
    golden_weights = GoldenWeightsService.get_golden_weights()

    if golden_weights == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='unknown',
                                                         value=None,
                                                         message='cannot determine what threw the error, check logs'),
                        status=400,
                        mimetype='application/json')

    elif golden_weights == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='unknown',
                                                              value=None,
                                                              message='cannot determine what threw the error, '
                                                                      'check the logs'),
                        status=404,
                        mimetype='application/json')

    else:
        return Response(response=json.dumps(golden_weights),
                        status=200,
                        mimetype='application/json')


@my_app.route('/NCAA/MB/golden_weights_calculator')
@door_staff
def calculate_golden_weights():
    golden_weights = GoldenWeightsService.determine_weights_precision()

    if golden_weights == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='unknown',
                                                         value=None,
                                                         message='cannot determine what threw the error, check logs'),
                        status=400,
                        mimetype='application/json')

    elif golden_weights == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='unknown',
                                                              value=None,
                                                              message='cannot determine what threw the error, check the logs'),
                        status=404,
                        mimetype='application/json')

    else:
        return Response(response=json.dumps(golden_weights),
                        status=200,
                        mimetype='application/json')


@my_app.route('/NCAA/MB/applied_golden_weights_output', methods=['DELETE'])
@door_staff
def delete_all_applied_golden_weights_models_output():
    AppliedGoldenWeightsOutputService.delete_all_applied_golden_weights_output_models()
    return Response(response=json.dumps({'Successfully deleted all of the golden weights output models': 'Check database to confirm'}),
                    status=202,
                    mimetype='application/json')


@my_app.route('/home')
@door_staff
def render_static():
    with open('templates/skeleton.html', 'r') as rf:
        file_contents = rf.read()

        all_schedule_models = ScheduleService.get_all_schedules()
        if all_schedule_models == Error.RESOURCE_NOT_FOUND:
            trs = "<tr></tr>"
            file_contents = file_contents.format(ncaa_results=trs)

        else:
            all_rows = HomeTemplateService.grab_all_schedule_rendering_information(all_schedule_models)
            if all_rows in [Error.INVALID_VALUE, Error.RESOURCE_NOT_FOUND]:
                trs = "<tr></tr>"
                file_contents = file_contents.format(ncaa_results=trs)

            else:
                file_contents = file_contents.format(ncaa_results=all_rows)

    with open('templates/home.html', 'w') as wf:
        wf.write(file_contents)

    return render_template('home.html')


if __name__ == '__main__':
    my_app.run('127.0.0.1', port=5000)


# todo - keep commented out, DANGEROUS!!! Will revert the database to original state
# @app.route('/create_database', methods=['POST'])
# def create_database():
#     from utils.database import db
#     from models.player_model import PlayerModel
#     from models.team_model import TeamModel
#     from models.season_model import SeasonModel
#
#     engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
#                               app.config['SQLALCHEMY_ENGINE_OPTIONS'])
#
#
#     todo - need to do it this way to accommodate the Foreign Key restraints
#     SeasonModel.metadata.drop_all(bind=engine)
#     TeamModel.metadata.drop_all(bind=engine)
#     PlayerModel.metadata.drop_all(bind=engine)
#
#     SeasonModel.metadata.create_all(bind=engine)
#     TeamModel.metadata.create_all(bind=engine)
#     PlayerModel.metadata.create_all(bind=engine)
#
#     return Response(response=json.dumps({'status': 'database successfully created'}))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)