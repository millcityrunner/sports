
from flask import request, Response

from services import sport_service as SportService

from components.Sport.serializers.CreateSportRequestData import CreateSportRequestData

from utils.create_app import app, logger
from utils.exceptions import Exception, Error

import json


@app.route('/sports', method=["POST"])
def create_sport():
    logger.info(f'Received the request to create a sport.')

    if not request.get_data() or request.get_data().decode() == '{}':
        logger.error(f'Failed to process the request to create a sport. Failed to supply a valid request body, '
                     f'request_body: {request.get_data()}')
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=request.get_data()),
                        status=400,
                        mimetype='application/json')

    try:
        logger.info(f'Attempted to serialize the request body for creating a sport.')
        req_data = CreateSportRequestData(data=request.get_json())

    except (ValueError, KeyError, AttributeError, TypeError) as e:
        logger.error(f'Failed to process the request to create a sport. Failed to supply a valid request body, '
                     f'request_body: {request.get_data()}')
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=str(e)),
                        status=400,
                        mimetype='application/json')

    logger.info(f'Successfully validated that the request body is valid for creating a sport. Attempting to create '
                f'the sport. req_data: {req_data.as_dict()}')
    sport_model = SportService.create_sport(req_data)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Attempted to create a sport, but received an INVALID_VALUE error from the Sports Service. '
                     f'req_data: {req_data.as_dict()}')
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=req_data),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.ALREADY_EXISTS:
        logger.error(f'Attempted to create a sport, but received an ALREADY_EXISTS error from the Sports Service. '
                     f'req_data: {req_data.as_dict()}')
        return Response(response=Exception.conflict(property_name='req_data',
                                                    value=req_data),
                        status=409,
                        mimetype='application/json')

    elif sport_model == Error.INTERNAL_SERVICE_ERROR:
        logger.error(f'Attempted to create a sport, but received an INTERNAL_SERVICE_ERROR error from the '
                     f'Sports Service. req_data: {req_data.as_dict()}')
        return Response(response=Exception.internal_service_error(property_name='req_data',
                                                                  value=req_data),
                        status=500,
                        mimetype='application/json')

    else:
        return Response(response=json.dumps(sport_model),
                        status=201,
                        mimetype='application/json')


@app.route('/sports')
def get_all_sports():
    pass

@app.route('/sports/{sport_id}')
def get_sport_by_id(sport_id):
    pass

@app.route('/sports/{sport_id}', method=['PUT'])
def update_sport(sport_id):
    pass

@app.route('/sports/{sport_id}', method=['DELETE'])
def delete_sport(sport_id):
    pass

@app.route('/sports/{sport_id}/seasons', method=["POST"])
def create_season(sport_id):
    pass

@app.route('/sports/{sport_id}/seasons')
def get_all_seasons(sport_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}')
def get_season_by_id(sport_id, season_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}', method=['PUT'])
def update_season(sport_id, season_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}', method=['DELETE'])
def delete_season(sport_id, season_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams', method=["POST"])
def create_team(sport_id, season_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams')
def get_all_teams(sport_id, season_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}')
def get_team_by_id(sport_id, season_id, team_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}', method=['PUT'])
def update_team(sport_id, season_id, team_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}', method=['DELETE'])
def delete_team(sport_id, season_id, team_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players', method=["POST"])
def create_player(sport_id, season_id, team_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players')
def get_all_players(sport_id, season_id, team_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}')
def get_player_by_id(sport_id, season_id, team_id, player_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}', method=['PUT'])
def update_player(sport_id, season_id, team_id, player_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}', method=['DELETE'])
def delete_player(sport_id, season_id, team_id, player_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/injury_reports', method=['POST'])
def create_injury_report(sport_id, season_id, team_id, player_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/injury_reports')
def get_all_injury_reports(sport_id, season_id, team_id, player_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/injury_reports/{injury_report_id}')
def get_injury_report_by_id(sport_id, season_id, team_id, player_id, injury_report_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/injury_reports/{injury_report_id}', method=['PUT'])
def update_injury_report(sport_id, season_id, team_id, player_id, injury_report_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/injury_reports/{injury_report_id}', method=['DELETE'])
def delete_injury_report(sport_id, season_id, team_id, player_id, injury_report_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/expectations', method=['POST'])
def create_player_expectation(sport_id, season_id, team_id, player_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/expectations')
def get_all_player_expectations(sport_id, season_id, team_id, player_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/expectations/{expectation_id}')
def get_player_expectation_by_id(sport_id, season_id, team_id, player_id, expectation_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/expectations/{expectation_id}', method=['PUT'])
def update_player_expectation(sport_id, season_id, team_id, player_id, expectation_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/expectations/{expectation_id}', method=['DELETE'])
def delete_player_expectation(sport_id, season_id, team_id, player_id, expectation_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules', method=["POST"])
def create_schedule(sport_id, season_id, team_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules')
def get_all_schedules(sport_id, season_id, team_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}')
def get_schedule_by_id(sport_id, season_id, team_id, schedule_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}', method=['PUT'])
def update_schedule(sport_id, season_id, team_id, schedule_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}', method=['DELETE'])
def delete_schedule(sport_id, season_id, team_id, schedule_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games', method=["POST"])
def create_game(sport_id, season_id, team_id, schedule_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games')
def get_all_games(sport_id, season_id, team_id, schedule_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}')
def get_game_by_id(sport_id, season_id, team_id, schedule_id, game_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}', method=['PUT'])
def update_game(sport_id, season_id, team_id, schedule_id, game_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}', method=['DELETE'])
def delete_game(sport_id, season_id, team_id, schedule_id, game_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/expectations', method=["POST"])
def create_game_expectation(sport_id, season_id, team_id, schedule_id, game_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/expectations')
def get_all_game_expectations(sport_id, season_id, team_id, schedule_id, game_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/expectations/{expectation_id}')
def get_game_expectation_by_id(sport_id, season_id, team_id, schedule_id, game_id, expectation_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/expectations/{expectation_id}', method=['PUT'])
def update_game_expectation(sport_id, season_id, team_id, schedule_id, game_id, expectation_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/expectations/{expectation_id}', method=['DELETE'])
def delete_game_expectation(sport_id, season_id, team_id, schedule_id, game_id, expectation_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/weather_reports', method=["POST"])
def create_weather_report(sport_id, season_id, team_id, schedule_id, game_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/weather_reports')
def get_all_weather_reports(sport_id, season_id, team_id, schedule_id, game_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/weather_reports/{weather_report_id}')
def get_weather_report_by_id(sport_id, season_id, team_id, schedule_id, game_id, weather_report_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/weather_reports/{weather_report_id}', method=['PUT'])
def update_weather_report(sport_id, season_id, team_id, schedule_id, game_id, weather_report_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/weather_reports/{weather_report_id}', method=['DELETE'])
def delete_weather_report(sport_id, season_id, team_id, schedule_id, game_id, weather_report_id):
    pass


if __name__ == '__main__':
    logger.info(f'Booting up the Sports API....')
    app.run(host='0.0.0.0', port=5000)

    logger.info(f'Successfully deployed the Sports API')