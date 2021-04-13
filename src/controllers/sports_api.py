
from flask import request, Response

from services import sport_service as SportService
from services import mlb_service as MLBService
from services import nfl_service as NFLService
from services import ncaamb_service as NCAAMBService

from components.Sport.serializers.CreateSportRequestData import CreateSportRequestData
from components.Sport.serializers.GetAllSportsRequestData import GetAllSportsRequestData
from components.Sport.serializers.UpdateSportRequestData import UpdateSportRequestData

from components.MLB.serializers.CreateSeasonRequestData import CreateSeasonRequestData
from components.MLB.serializers.GetAllSeasonsRequestData import GetAllSeasonsRequestData

from components.MLB.serializers.GetAllTeamsRequestData import GetAllTeamsRequestData

from components.MLB.serializers.GetAllPlayersRequestData import GetAllPlayerRequestData


from utils.create_app import app, logger
from utils.exceptions import Exception, Error
from utils.constants import NFL_CONSTANT, NCAAMB_CONSTANT, NBA_CONSTANT, MLB_CONSTANT

import json


@app.route('/sports', methods=["POST"])
def create_sport():
    logger.info(f'Received the request to create a sport.')

    if not request.get_data() or request.get_data().decode() == '{}':
        logger.error(f'Failed to process the request to create a sport. Failed to supply a valid request body, '
                     f'request_body: {request.get_data()}')
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    try:
        logger.info(f'Attempted to serialize the request body for creating a sport.')
        req_data = CreateSportRequestData(data=request.get_data().decode())

    except (ValueError, KeyError, AttributeError, TypeError) as e:
        logger.error(f'Failed to process the request to create a sport. Failed to supply a valid request body, '
                     f'request_body: {request.get_data().decode()}')
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
        logger.info(f'Successfully created a sport model. sport_model: {sport_model.as_dict()}')
        return Response(response=json.dumps(sport_model),
                        status=201,
                        mimetype='application/json')


@app.route('/sports')
def get_all_sports():
    logger.info(f'Received the request to get all sports.')

    filters = request.args

    if filters:
        logger.info(f'While attempting to retrieve all of the sports, it appears request params were passed along. '
                    f'Serializing the request body, before continuing with call to the database. '
                    f'request.args: {filters}')
        try:
            req_data = GetAllSportsRequestData(data=filters)

        except (ValueError, AttributeError, KeyError, TypeError) as e:
            logger.error(f'Failed to pass the serializer when requesting to get all of the sports. '
                         f'request.args: {filters}')
            return Response(response=Exception.invalid_value(property_name='request.args',
                                                             value=str(e)),
                            status=400,
                            mimetype='application/json')

        logger.info(f'Successfully validated that the request body conforms with the expected get all sports '
                    f'serializer. Passing the request onto the service. req_data: {req_data.as_dict()}')
        sport_models = SportService.get_all_sports(**req_data.as_dict())

    else:
        logger.info(f'There was no request parameters present when attempting to retrieve all of the sports. '
                    f'Passing the request onto the service.')
        sport_models = SportService.get_all_sports()

    if sport_models == Error.INVALID_VALUE:
        logger.error(f'Received an INVALID_VALUE from the call to the service, when retrieving all of the '
                     f'sport models. request_body: {request.get_data().decode()}')
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=sport_models),
                        status=400,
                        mimetype='application/json')

    elif sport_models == Error.EMPTY_SET:
        logger.error(f'Received an EMPTY_SET from the call to the service, when retrieving all of the '
                     f'sport models. request_body: {request.get_data().decode()}')
        return Response(response=Exception.empty_set(),
                        status=409,
                        mimetype='application/json')

    else:
        logger.info(f'Successfully retrieved all of the sport models from the database. sport_models: {sport_models}')
        return Response(response=json.dumps(sport_models),
                        status=200,
                        mimetype='application/json')


@app.route('/sports/{sport_id}')
def get_sport_by_id(sport_id):
    logger.info(f'Received the request to get a sport. '
                f'Passing the request onto the service. sport_id: {sport_id}')
    sport_model = SportService.get_sport_by_id(sport_id=sport_id, return_as_model=False)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Received an INVALID_VALUE from the call to the service, when retrieving a '
                     f'sport model. sport_id: {sport_id}')
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=sport_models),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.EMPTY_SET:
        logger.error(f'Received an EMPTY_SET from the call to the service, when retrieving a '
                     f'sport model. sport_id: {sport_id}')
        return Response(response=Exception.empty_set(),
                        status=409,
                        mimetype='application/json')

    else:
        logger.info(f'Successfully retrieved a sport model from the database. sport_model: {sport_model}')
        return Response(response=json.dumps(sport_model),
                        status=200,
                        mimetype='application/json')


@app.route('/sports/{sport_id}', methods=['PUT'])
def update_sport(sport_id):
    logger.info(f'Received the request to update a sport model. sport_id: {sport_id}')

    if not request.get_data() or request.get_data().decode() == '{}':
        logger.error(f'Failed to process the request to update a sport. Failed to supply a valid request body, '
                     f'request_body: {request.get_data()}')
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=request.get_data()),
                        status=400,
                        mimetype='application/json')

    try:
        logger.info(f'Attempted to serialize the request body for updating a sport.')
        req_data = UpdateSportRequestData(data=request.get_data().decode())

    except (ValueError, KeyError, AttributeError, TypeError) as e:
        logger.error(f'Failed to process the request to update a sport. Failed to supply a valid request body, '
                     f'request_body: {request.get_data()}')
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=str(e)),
                        status=400,
                        mimetype='application/json')

    logger.info(f'Successfully validated the request body for updating a sport. sport_id: {sport_id}, '
                f'req_data: {req_data.as_dict()}')

    logger.info(f'Pasing the request onto the service to update the sport model. sport_id: {sport_id}, '
                f'req_data: {req_data.as_dict()}')
    sport_model = SportService.update_sport(sport_id=sport_id, name=req_data.name)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Received an INVALID_VALUE from the call to the service, when updating a '
                     f'sport model. sport_id: {sport_id}, name: {req_data.name}')
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=sport_model),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.EMPTY_SET:
        logger.error(f'Received an EMPTY_SET from the call to the service, when updating a '
                     f'sport model. sport_id: {sport_id}')
        return Response(response=Exception.empty_set(),
                        status=409,
                        mimetype='application/json')

    else:
        logger.info(f'Successfully updated a sport model from the database. sport_model: {sport_model}')
        return Response(response=json.dumps(sport_model),
                        status=202,
                        mimetype='application/json')


@app.route('/sports/{sport_id}', methods=['DELETE'])
def delete_sport(sport_id):
    logger.info(f'Received the request to delete a sport model. sport_id: {sport_id}')

    logger.info(f'Passing the request onto the service, to delete a sport. sport_id: {sport_id}')
    sport_model = SportService.delete_sport(sport_id=sport_id)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Failed to delete a sport. Received an INVALID_VALUE from the call to the service. '
                     f'sport_id: {sport_id}')
        return Response(response=Exception.invalid_value(property_name='req_data',
                                                         value=sport_id),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.RESOURCE_NOT_FOUND:
        logger.error(f'Failed to delete a sport. Received an INVALID_VALUE from the call to the service. '
                     f'sport_id: {sport_id}')
        return Response(response=Exception.resource_not_found(property_name='sport_model',
                                                              value=sport_id),
                        status=404,
                        mimetype='application/json')

    else:
        logger.info(f'Successfully deleted a sport model. sport_id: {sport_id}, sport_model: {sport_model.as_dict()}')
        return Response(response=json.dumps(sport_model),
                        status=204,
                        mimetype='application/json')


@app.route('/sports/{sport_id}/seasons', methods=["POST"])
def create_season(sport_id):
    logger.info(f'Received the request to create a season.')

    logger.info(f'Attempting to retrieve a sport by id. sport_id: {sport_id}')
    sport_model = SportService.get_sport_by_id(sport_id=sport_id)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Failed to pass in a valid sport_id when attempting to get a sport by id. sport_id: {sport_id}')
        return Response(response=Exception.invalid_value(property_name='sport_id',
                                                         value=sport_id),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.RESOURCE_NOT_FOUND:
        logger.error(f'Failed to locate a sport model with the specified sport_id. sport_id: {sport_id}')
        return Response(response=Exception.resource_not_found(property_name='sport_id',
                                                              value=sport_id),
                        status=404,
                        mimetype='application/json')

    logger.info(f'Successfully validated that the sport_id does conform with an existing sport model. '
                f'Attempting to route the request to the correct service. sport_model: {sport_model}')
    if sport_model.get('name') == MLB_CONSTANT:
        Service = MLBService

    elif sport_model.get('name') == NFL_CONSTANT:
        Service = NFLService

    elif sport_model.get('name') == NCAAMB_CONSTANT:
        Service = NCAAMBService

    # elif sport_model.get('name') == NBA_CONSTANT:
    #     Service = NBAService

    else:
        logger.error(f'Failed to determine which service the sport model belongs to. sport_model: {sport_model}')
        return Response(response=Exception.failed_dependency(),
                        status=424,
                        mimetype='application/json')

    logger.info(f'Successfully determined the appropriate service for the sport model. sport_model: {sport_model}')

    logger.info(f'Attempting to create a season, by passing along the request body to the appropriate service. '
                f'sport_model: {sport_model}, request_body: {request.get_data().decode()}')
    season_model = Service.create_season(request.get_data().decode(), sport_id=sport_id)

    if season_model == Error.INVALID_VALUE:
        logger.error(f'Attempted to create a season, but received an INVALID_VALUE error from the Service. '
                     f'request_body: {request.get_data().decode()}')
        return Response(response=Exception.invalid_value(property_name='request_body',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    elif season_model == Error.ALREADY_EXISTS:
        logger.error(f'Attempted to create a season, but received an ALREADY_EXISTS error from the Service. '
                     f'request_body: {request.get_data().decode().as_dict()}')
        return Response(response=Exception.conflict(property_name='request_body',
                                                    value=request.get_data().decode()),
                        status=409,
                        mimetype='application/json')

    elif season_model == Error.INTERNAL_SERVICE_ERROR:
        logger.error(f'Attempted to create a season, but received an INTERNAL_SERVICE_ERROR error from the '
                     f'Service. request_body: {request.get_data().decode().as_dict()}')
        return Response(response=Exception.internal_service_error(property_name='request_body',
                                                                  value=request.get_data().decode()),
                        status=500,
                        mimetype='application/json')

    else:
        logger.info(f'Successfully created a season model. season_model: {season_model.as_dict()}, '
                    f'sport_model: {sport_model}')
        return Response(response=json.dumps(season_model),
                        status=201,
                        mimetype='application/json')


@app.route('/sports/{sport_id}/seasons')
def get_all_seasons(sport_id):
    logger.info(f'Received the request to get all seasons.')

    logger.info(f'Attempting to retrieve a sport by id. sport_id: {sport_id}')
    sport_model = SportService.get_sport_by_id(sport_id=sport_id)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Failed to pass in a valid sport_id when attempting to get a sport by id. sport_id: {sport_id}')
        return Response(response=Exception.invalid_value(property_name='sport_id',
                                                         value=sport_id),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.RESOURCE_NOT_FOUND:
        logger.error(f'Failed to locate a sport model with the specified sport_id. sport_id: {sport_id}')
        return Response(response=Exception.resource_not_found(property_name='sport_id',
                                                              value=sport_id),
                        status=404,
                        mimetype='application/json')

    logger.info(f'Successfully validated that the sport_id does conform with an existing sport model. '
                f'Attempting to route the request to the correct service. sport_model: {sport_model}')
    if sport_model.get('name') == MLB_CONSTANT:
        Service = MLBService

    elif sport_model.get('name') == NFL_CONSTANT:
        Service = NFLService

    elif sport_model.get('name') == NCAAMB_CONSTANT:
        Service = NCAAMBService

    # elif sport_model.get('name') == NBA_CONSTANT:
    #     Service = NBAService

    else:
        logger.error(f'Failed to determine which service the sport model belongs to. sport_model: {sport_model}')
        return Response(response=Exception.failed_dependency(),
                        status=424,
                        mimetype='application/json')

    logger.info(f'Successfully determined the appropriate service for the sport model. sport_model: {sport_model}')

    filters = request.args

    if filters:
        logger.info(f'While attempting to retrieve all of the seasons, it appears request params were passed along. '
                    f'Serializing the request body, before continuing with call to the database. '
                    f'request.args: {filters}')
        try:
            req_data = GetAllSeasonsRequestData(data=filters)

        except (ValueError, AttributeError, KeyError, TypeError) as e:
            logger.error(f'Failed to pass the serializer when requesting to get all of the seasons. '
                         f'request.args: {filters}')
            return Response(response=Exception.invalid_value(property_name='request.args',
                                                             value=str(e)),
                            status=400,
                            mimetype='application/json')

        logger.info(f'Successfully validated that the request params conforms with the expected get all seasons '
                    f'serializer. Passing the request onto the service. req_data: {req_data.as_dict()}')
        season_models = Service.get_all_seasons(**req_data.as_dict())

    else:
        logger.info(f'There was no request parameters present when attempting to retrieve all of the seasons. '
                    f'Passing the request onto the service.')
        season_models = Service.get_all_seasons()

    if season_models == Error.EMPTY_SET:
        return Response(response=Exception.empty_set(),
                        status=404,
                        mimetype='application/json')

    return Response(response=json.dumps(season_models),
                    status=200,
                    mimetype='application/json')


@app.route('/sports/{sport_id}/seasons/{season_id}')
def get_season_by_id(sport_id, season_id):
    logger.info(f'Received the request to get a season by id.')

    logger.info(f'Attempting to retrieve a sport by id. sport_id: {sport_id}')
    sport_model = SportService.get_sport_by_id(sport_id=sport_id)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Failed to pass in a valid sport_id when attempting to get a sport by id. sport_id: {sport_id}')
        return Response(response=Exception.invalid_value(property_name='sport_id',
                                                         value=sport_id),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.RESOURCE_NOT_FOUND:
        logger.error(f'Failed to locate a sport model with the specified sport_id. sport_id: {sport_id}')
        return Response(response=Exception.resource_not_found(property_name='sport_id',
                                                              value=sport_id),
                        status=404,
                        mimetype='application/json')

    logger.info(f'Successfully validated that the sport_id does conform with an existing sport model. '
                f'Attempting to route the request to the correct service. sport_model: {sport_model}')
    if sport_model.get('name') == MLB_CONSTANT:
        Service = MLBService

    elif sport_model.get('name') == NFL_CONSTANT:
        Service = NFLService

    elif sport_model.get('name') == NCAAMB_CONSTANT:
        Service = NCAAMBService

    # elif sport_model.get('name') == NBA_CONSTANT:
    #     Service = NBAService

    else:
        logger.error(f'Failed to determine which service the sport model belongs to. sport_model: {sport_model}')
        return Response(response=Exception.failed_dependency(),
                        status=424,
                        mimetype='application/json')

    logger.info(f'Successfully determined the appropriate service for the sport model. sport_model: {sport_model}')

    season_model = Service.get_season_by_id(season_id=season_id)

    if season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    return Response(response=json.dumps(season_model),
                    status=200,
                    mimetype='application/json')


@app.route('/sports/{sport_id}/seasons/{season_id}', methods=['PUT'])
def update_season(sport_id, season_id):
    logger.info(f'Received the request to update a season.')

    logger.info(f'Attempting to retrieve a sport by id. sport_id: {sport_id}')
    sport_model = SportService.get_sport_by_id(sport_id=sport_id)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Failed to pass in a valid sport_id when attempting to get a sport by id. sport_id: {sport_id}')
        return Response(response=Exception.invalid_value(property_name='sport_id',
                                                         value=sport_id),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.RESOURCE_NOT_FOUND:
        logger.error(f'Failed to locate a sport model with the specified sport_id. sport_id: {sport_id}')
        return Response(response=Exception.resource_not_found(property_name='sport_id',
                                                              value=sport_id),
                        status=404,
                        mimetype='application/json')

    logger.info(f'Successfully validated that the sport_id does conform with an existing sport model. '
                f'Attempting to route the request to the correct service. sport_model: {sport_model}')
    if sport_model.get('name') == MLB_CONSTANT:
        Service = MLBService

    elif sport_model.get('name') == NFL_CONSTANT:
        Service = NFLService

    elif sport_model.get('name') == NCAAMB_CONSTANT:
        Service = NCAAMBService

    # elif sport_model.get('name') == NBA_CONSTANT:
    #     Service = NBAService

    else:
        logger.error(f'Failed to determine which service the sport model belongs to. sport_model: {sport_model}')
        return Response(response=Exception.failed_dependency(),
                        status=424,
                        mimetype='application/json')

    logger.info(f'Successfully determined the appropriate service for the sport model. sport_model: {sport_model}')

    season_model = Service.update_season(season_id=season_id, request_body=request.get_data().decode())

    if season_model == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='request_body',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    elif season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    return Response(response=json.dumps(season_model),
                    status=202,
                    mimetype='application/json')


@app.route('/sports/{sport_id}/seasons/{season_id}', methods=['DELETE'])
def delete_season(sport_id, season_id):
    logger.info(f'Received the request to update a team.')

    logger.info(f'Attempting to retrieve a sport by id. sport_id: {sport_id}')
    sport_model = SportService.get_sport_by_id(sport_id=sport_id)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Failed to pass in a valid sport_id when attempting to get a sport by id. sport_id: {sport_id}')
        return Response(response=Exception.invalid_value(property_name='sport_id',
                                                         value=sport_id),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.RESOURCE_NOT_FOUND:
        logger.error(f'Failed to locate a sport model with the specified sport_id. sport_id: {sport_id}')
        return Response(response=Exception.resource_not_found(property_name='sport_id',
                                                              value=sport_id),
                        status=404,
                        mimetype='application/json')

    logger.info(f'Successfully validated that the sport_id does conform with an existing sport model. '
                f'Attempting to route the request to the correct service. sport_model: {sport_model}')
    if sport_model.get('name') == MLB_CONSTANT:
        Service = MLBService

    elif sport_model.get('name') == NFL_CONSTANT:
        Service = NFLService

    elif sport_model.get('name') == NCAAMB_CONSTANT:
        Service = NCAAMBService

    # elif sport_model.get('name') == NBA_CONSTANT:
    #     Service = NBAService

    else:
        logger.error(f'Failed to determine which service the sport model belongs to. sport_model: {sport_model}')
        return Response(response=Exception.failed_dependency(),
                        status=424,
                        mimetype='application/json')

    logger.info(f'Successfully determined the appropriate service for the sport model. sport_model: {sport_model}')

    season_model = Service.delete_season(season_id=season_id)

    if season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    return Response(response=json.dumps(season_model),
                    status=204,
                    mimetype='application/json')


@app.route('/sports/{sport_id}/seasons/{season_id}/teams', methods=["POST"])
def create_team(sport_id, season_id):
    logger.info(f'Received the request to create a team.')

    logger.info(f'Attempting to retrieve a sport by id. sport_id: {sport_id}')
    sport_model = SportService.get_sport_by_id(sport_id=sport_id)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Failed to pass in a valid sport_id when attempting to get a sport by id. sport_id: {sport_id}')
        return Response(response=Exception.invalid_value(property_name='sport_id',
                                                         value=sport_id),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.RESOURCE_NOT_FOUND:
        logger.error(f'Failed to locate a sport model with the specified sport_id. sport_id: {sport_id}')
        return Response(response=Exception.resource_not_found(property_name='sport_id',
                                                              value=sport_id),
                        status=404,
                        mimetype='application/json')

    logger.info(f'Successfully validated that the sport_id does conform with an existing sport model. '
                f'Attempting to route the request to the correct service. sport_model: {sport_model}')
    if sport_model.get('name') == MLB_CONSTANT:
        Service = MLBService

    elif sport_model.get('name') == NFL_CONSTANT:
        Service = NFLService

    elif sport_model.get('name') == NCAAMB_CONSTANT:
        Service = NCAAMBService

    # elif sport_model.get('name') == NBA_CONSTANT:
    #     Service = NBAService

    else:
        logger.error(f'Failed to determine which service the sport model belongs to. sport_model: {sport_model}')
        return Response(response=Exception.failed_dependency(),
                        status=424,
                        mimetype='application/json')

    logger.info(f'Successfully determined the appropriate service for the sport model. sport_model: {sport_model}')

    season_model = Service.get_season_by_id(season_id=season_id)

    if season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    team_model = Service.create_team(request_body=request.get_data().decode(), season_id=season_id)

    if team_model == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='request_body',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    return Response(response=json.dumps(team_model),
                    status=201,
                    mimetype='application/json')


@app.route('/sports/{sport_id}/seasons/{season_id}/teams')
def get_all_teams(sport_id, season_id):
    logger.info(f'Received the request to get all teams.')

    logger.info(f'Attempting to retrieve a sport by id. sport_id: {sport_id}')
    sport_model = SportService.get_sport_by_id(sport_id=sport_id)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Failed to pass in a valid sport_id when attempting to get a sport by id. sport_id: {sport_id}')
        return Response(response=Exception.invalid_value(property_name='sport_id',
                                                         value=sport_id),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.RESOURCE_NOT_FOUND:
        logger.error(f'Failed to locate a sport model with the specified sport_id. sport_id: {sport_id}')
        return Response(response=Exception.resource_not_found(property_name='sport_id',
                                                              value=sport_id),
                        status=404,
                        mimetype='application/json')

    logger.info(f'Successfully validated that the sport_id does conform with an existing sport model. '
                f'Attempting to route the request to the correct service. sport_model: {sport_model}')
    if sport_model.get('name') == MLB_CONSTANT:
        Service = MLBService

    elif sport_model.get('name') == NFL_CONSTANT:
        Service = NFLService

    elif sport_model.get('name') == NCAAMB_CONSTANT:
        Service = NCAAMBService

    # elif sport_model.get('name') == NBA_CONSTANT:
    #     Service = NBAService

    else:
        logger.error(f'Failed to determine which service the sport model belongs to. sport_model: {sport_model}')
        return Response(response=Exception.failed_dependency(),
                        status=424,
                        mimetype='application/json')

    logger.info(f'Successfully determined the appropriate service for the sport model. sport_model: {sport_model}')

    season_model = Service.get_season_by_id(season_id=season_id)

    if season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    filters = request.args

    if filters:
        logger.info(f'While attempting to retrieve all of the teams, it appears request params were passed along. '
                    f'Serializing the request body, before continuing with call to the database. '
                    f'request.args: {filters}')
        try:
            req_data = GetAllTeamsRequestData(data=filters)

        except (ValueError, AttributeError, KeyError, TypeError) as e:
            logger.error(f'Failed to pass the serializer when requesting to get all of the teams. '
                         f'request.args: {filters}')
            return Response(response=Exception.invalid_value(property_name='request.args',
                                                             value=str(e)),
                            status=400,
                            mimetype='application/json')

        logger.info(f'Successfully validated that the request params conforms with the expected get all teams '
                    f'serializer. Passing the request onto the service. req_data: {req_data.as_dict()}')
        team_models = Service.get_all_teams(**req_data.as_dict())

    else:
        logger.info(f'There was no request parameters present when attempting to retrieve all of the teams. '
                    f'Passing the request onto the service.')
        team_models = Service.get_all_teams()

    if team_models == Error.EMPTY_SET:
        return Response(response=Exception.empty_set(),
                        status=404,
                        mimetype='application/json')

    return Response(response=json.dumps(team_models),
                    status=200,
                    mimetype='application/json')


@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}')
def get_team_by_id(sport_id, season_id, team_id):
    logger.info(f'Received the request to get a team by id.')

    logger.info(f'Attempting to retrieve a sport by id. sport_id: {sport_id}')
    sport_model = SportService.get_sport_by_id(sport_id=sport_id)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Failed to pass in a valid sport_id when attempting to get a sport by id. sport_id: {sport_id}')
        return Response(response=Exception.invalid_value(property_name='sport_id',
                                                         value=sport_id),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.RESOURCE_NOT_FOUND:
        logger.error(f'Failed to locate a sport model with the specified sport_id. sport_id: {sport_id}')
        return Response(response=Exception.resource_not_found(property_name='sport_id',
                                                              value=sport_id),
                        status=404,
                        mimetype='application/json')

    logger.info(f'Successfully validated that the sport_id does conform with an existing sport model. '
                f'Attempting to route the request to the correct service. sport_model: {sport_model}')
    if sport_model.get('name') == MLB_CONSTANT:
        Service = MLBService

    elif sport_model.get('name') == NFL_CONSTANT:
        Service = NFLService

    elif sport_model.get('name') == NCAAMB_CONSTANT:
        Service = NCAAMBService

    # elif sport_model.get('name') == NBA_CONSTANT:
    #     Service = NBAService

    else:
        logger.error(f'Failed to determine which service the sport model belongs to. sport_model: {sport_model}')
        return Response(response=Exception.failed_dependency(),
                        status=424,
                        mimetype='application/json')

    logger.info(f'Successfully determined the appropriate service for the sport model. sport_model: {sport_model}')

    season_model = Service.get_season_by_id(season_id=season_id)

    if season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    team_model = Service.get_team_by_id(team_id=team_id)

    if team_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.invalid_value(property_name='team_id',
                                                         value=team_id),
                        status=404,
                        mimetype='application/json')

    return Response(response=json.dumps(team_model),
                    status=200,
                    mimetype='application/json')


@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}', methods=['PUT'])
def update_team(sport_id, season_id, team_id):
    logger.info(f'Received the request to update a team.')

    logger.info(f'Attempting to retrieve a sport by id. sport_id: {sport_id}')
    sport_model = SportService.get_sport_by_id(sport_id=sport_id)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Failed to pass in a valid sport_id when attempting to get a sport by id. sport_id: {sport_id}')
        return Response(response=Exception.invalid_value(property_name='sport_id',
                                                         value=sport_id),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.RESOURCE_NOT_FOUND:
        logger.error(f'Failed to locate a sport model with the specified sport_id. sport_id: {sport_id}')
        return Response(response=Exception.resource_not_found(property_name='sport_id',
                                                              value=sport_id),
                        status=404,
                        mimetype='application/json')

    logger.info(f'Successfully validated that the sport_id does conform with an existing sport model. '
                f'Attempting to route the request to the correct service. sport_model: {sport_model}')
    if sport_model.get('name') == MLB_CONSTANT:
        Service = MLBService

    elif sport_model.get('name') == NFL_CONSTANT:
        Service = NFLService

    elif sport_model.get('name') == NCAAMB_CONSTANT:
        Service = NCAAMBService

    # elif sport_model.get('name') == NBA_CONSTANT:
    #     Service = NBAService

    else:
        logger.error(f'Failed to determine which service the sport model belongs to. sport_model: {sport_model}')
        return Response(response=Exception.failed_dependency(),
                        status=424,
                        mimetype='application/json')

    logger.info(f'Successfully determined the appropriate service for the sport model. sport_model: {sport_model}')

    season_model = Service.get_season_by_id(season_id=season_id)

    if season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    team_model = Service.update_team(team_id, request_body=request.get_data().decode())

    if team_model == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='request_body',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    elif team_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='team_id',
                                                              value=team_id),
                        status=404,
                        mimetype='application/json')

    return Response(response=json.dumps(team_model),
                    status=202,
                    mimetype='application/json')


@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}', methods=['DELETE'])
def delete_team(sport_id, season_id, team_id):
    logger.info(f'Received the request to delete a team.')

    logger.info(f'Attempting to retrieve a sport by id. sport_id: {sport_id}')
    sport_model = SportService.get_sport_by_id(sport_id=sport_id)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Failed to pass in a valid sport_id when attempting to get a sport by id. sport_id: {sport_id}')
        return Response(response=Exception.invalid_value(property_name='sport_id',
                                                         value=sport_id),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.RESOURCE_NOT_FOUND:
        logger.error(f'Failed to locate a sport model with the specified sport_id. sport_id: {sport_id}')
        return Response(response=Exception.resource_not_found(property_name='sport_id',
                                                              value=sport_id),
                        status=404,
                        mimetype='application/json')

    logger.info(f'Successfully validated that the sport_id does conform with an existing sport model. '
                f'Attempting to route the request to the correct service. sport_model: {sport_model}')
    if sport_model.get('name') == MLB_CONSTANT:
        Service = MLBService

    elif sport_model.get('name') == NFL_CONSTANT:
        Service = NFLService

    elif sport_model.get('name') == NCAAMB_CONSTANT:
        Service = NCAAMBService

    # elif sport_model.get('name') == NBA_CONSTANT:
    #     Service = NBAService

    else:
        logger.error(f'Failed to determine which service the sport model belongs to. sport_model: {sport_model}')
        return Response(response=Exception.failed_dependency(),
                        status=424,
                        mimetype='application/json')

    logger.info(f'Successfully determined the appropriate service for the sport model. sport_model: {sport_model}')

    season_model = Service.get_season_by_id(season_id=season_id)

    if season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    team_model = Service.delete_team(team_id=team_id)

    if team_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='team_id',
                                                              value=team_id),
                        status=404,
                        mimetype='application/json')

    return Response(response=json.dumps(team_model),
                    status=202,
                    mimetype='application/json')


@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players', methods=["POST"])
def create_player(sport_id, season_id, team_id):
    logger.info(f'Received the request to create a player.')

    logger.info(f'Attempting to retrieve a sport by id. sport_id: {sport_id}')
    sport_model = SportService.get_sport_by_id(sport_id=sport_id)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Failed to pass in a valid sport_id when attempting to get a sport by id. sport_id: {sport_id}')
        return Response(response=Exception.invalid_value(property_name='sport_id',
                                                         value=sport_id),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.RESOURCE_NOT_FOUND:
        logger.error(f'Failed to locate a sport model with the specified sport_id. sport_id: {sport_id}')
        return Response(response=Exception.resource_not_found(property_name='sport_id',
                                                              value=sport_id),
                        status=404,
                        mimetype='application/json')

    logger.info(f'Successfully validated that the sport_id does conform with an existing sport model. '
                f'Attempting to route the request to the correct service. sport_model: {sport_model}')
    if sport_model.get('name') == MLB_CONSTANT:
        Service = MLBService

    elif sport_model.get('name') == NFL_CONSTANT:
        Service = NFLService

    elif sport_model.get('name') == NCAAMB_CONSTANT:
        Service = NCAAMBService

    # elif sport_model.get('name') == NBA_CONSTANT:
    #     Service = NBAService

    else:
        logger.error(f'Failed to determine which service the sport model belongs to. sport_model: {sport_model}')
        return Response(response=Exception.failed_dependency(),
                        status=424,
                        mimetype='application/json')

    logger.info(f'Successfully determined the appropriate service for the sport model. sport_model: {sport_model}')

    season_model = Service.get_season_by_id(season_id=season_id)

    if season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    team_model = Service.get_team_by_id(team_id=team_id)

    if team_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='team_id',
                                                              value=team_id),
                        status=404,
                        mimetype='application/json')

    player_model = Service.create_player(request_body=request.get_data().decode(), team_id=team_id)

    if player_model == Error.INVALID_VALUE:
        return Response(response=Exception.invalid_value(property_name='request_body',
                                                         value=request.get_data().decode()),
                        status=400,
                        mimetype='application/json')

    return Response(response=json.dumps(player_model),
                    status=201,
                    mimetype='application/json')


@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players')
def get_all_players(sport_id, season_id, team_id):
    logger.info(f'Received the request to create a player.')

    logger.info(f'Attempting to retrieve a sport by id. sport_id: {sport_id}')
    sport_model = SportService.get_sport_by_id(sport_id=sport_id)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Failed to pass in a valid sport_id when attempting to get a sport by id. sport_id: {sport_id}')
        return Response(response=Exception.invalid_value(property_name='sport_id',
                                                         value=sport_id),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.RESOURCE_NOT_FOUND:
        logger.error(f'Failed to locate a sport model with the specified sport_id. sport_id: {sport_id}')
        return Response(response=Exception.resource_not_found(property_name='sport_id',
                                                              value=sport_id),
                        status=404,
                        mimetype='application/json')

    logger.info(f'Successfully validated that the sport_id does conform with an existing sport model. '
                f'Attempting to route the request to the correct service. sport_model: {sport_model}')
    if sport_model.get('name') == MLB_CONSTANT:
        Service = MLBService

    elif sport_model.get('name') == NFL_CONSTANT:
        Service = NFLService

    elif sport_model.get('name') == NCAAMB_CONSTANT:
        Service = NCAAMBService

    # elif sport_model.get('name') == NBA_CONSTANT:
    #     Service = NBAService

    else:
        logger.error(f'Failed to determine which service the sport model belongs to. sport_model: {sport_model}')
        return Response(response=Exception.failed_dependency(),
                        status=424,
                        mimetype='application/json')

    logger.info(f'Successfully determined the appropriate service for the sport model. sport_model: {sport_model}')

    season_model = Service.get_season_by_id(season_id=season_id)

    if season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    team_model = Service.get_team_by_id(team_id=team_id)

    if team_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='team_id',
                                                              value=team_id),
                        status=404,
                        mimetype='application/json')

    filters = request.args

    if filters:
        logger.info(f'While attempting to retrieve all of the players, it appears request params were passed along. '
                    f'Serializing the request body, before continuing with call to the database. '
                    f'request.args: {filters}')
        try:
            req_data = GetAllPlayersRequestData(data=filters)

        except (ValueError, AttributeError, KeyError, TypeError) as e:
            logger.error(f'Failed to pass the serializer when requesting to get all of the players. '
                         f'request.args: {filters}')
            return Response(response=Exception.invalid_value(property_name='request.args',
                                                             value=str(e)),
                            status=400,
                            mimetype='application/json')

        logger.info(f'Successfully validated that the request params conforms with the expected get all players '
                    f'serializer. Passing the request onto the service. req_data: {req_data.as_dict()}')
        player_models = Service.get_all_players(**req_data.as_dict())

    else:
        logger.info(f'There was no request parameters present when attempting to retrieve all of the players. '
                    f'Passing the request onto the service.')
        player_models = Service.get_all_players()

    if player_models == Error.EMPTY_SET:
        return Response(response=Exception.empty_set(),
                        status=404,
                        mimetype='application/json')

    return Response(response=json.dumps(player_models),
                    status=200,
                    mimetype='application/json')


@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}')
def get_player_by_id(sport_id, season_id, team_id, player_id):
    logger.info(f'Received the request to create a player.')

    logger.info(f'Attempting to retrieve a sport by id. sport_id: {sport_id}')
    sport_model = SportService.get_sport_by_id(sport_id=sport_id)

    if sport_model == Error.INVALID_VALUE:
        logger.error(f'Failed to pass in a valid sport_id when attempting to get a sport by id. sport_id: {sport_id}')
        return Response(response=Exception.invalid_value(property_name='sport_id',
                                                         value=sport_id),
                        status=400,
                        mimetype='application/json')

    elif sport_model == Error.RESOURCE_NOT_FOUND:
        logger.error(f'Failed to locate a sport model with the specified sport_id. sport_id: {sport_id}')
        return Response(response=Exception.resource_not_found(property_name='sport_id',
                                                              value=sport_id),
                        status=404,
                        mimetype='application/json')

    logger.info(f'Successfully validated that the sport_id does conform with an existing sport model. '
                f'Attempting to route the request to the correct service. sport_model: {sport_model}')
    if sport_model.get('name') == MLB_CONSTANT:
        Service = MLBService

    elif sport_model.get('name') == NFL_CONSTANT:
        Service = NFLService

    elif sport_model.get('name') == NCAAMB_CONSTANT:
        Service = NCAAMBService

    # elif sport_model.get('name') == NBA_CONSTANT:
    #     Service = NBAService

    else:
        logger.error(f'Failed to determine which service the sport model belongs to. sport_model: {sport_model}')
        return Response(response=Exception.failed_dependency(),
                        status=424,
                        mimetype='application/json')

    logger.info(f'Successfully determined the appropriate service for the sport model. sport_model: {sport_model}')

    season_model = Service.get_season_by_id(season_id=season_id)

    if season_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='season_id',
                                                              value=season_id),
                        status=404,
                        mimetype='application/json')

    team_model = Service.get_team_by_id(team_id=team_id)

    if team_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='team_id',
                                                              value=team_id),
                        status=404,
                        mimetype='application/json')

    player_model = Service.get_player_by_id(player_id=player_id)

    if player_model == Error.RESOURCE_NOT_FOUND:
        return Response(response=Exception.resource_not_found(property_name='player_id',
                                                              value=player_id),
                        status=404,
                        mimetype='application/json')

    return Response(response=json.dumps(player_model),
                    status=200,
                    mimetype='application/json')


@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}', methods=['PUT'])
def update_player(sport_id, season_id, team_id, player_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}', methods=['DELETE'])
def delete_player(sport_id, season_id, team_id, player_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/injury_reports', methods=['POST'])
def create_injury_report(sport_id, season_id, team_id, player_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/injury_reports')
def get_all_injury_reports(sport_id, season_id, team_id, player_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/injury_reports/{injury_report_id}')
def get_injury_report_by_id(sport_id, season_id, team_id, player_id, injury_report_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/injury_reports/{injury_report_id}', methods=['PUT'])
def update_injury_report(sport_id, season_id, team_id, player_id, injury_report_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/injury_reports/{injury_report_id}', methods=['DELETE'])
def delete_injury_report(sport_id, season_id, team_id, player_id, injury_report_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/expectations', methods=['POST'])
def create_player_expectation(sport_id, season_id, team_id, player_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/expectations')
def get_all_player_expectations(sport_id, season_id, team_id, player_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/expectations/{expectation_id}')
def get_player_expectation_by_id(sport_id, season_id, team_id, player_id, expectation_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/expectations/{expectation_id}', methods=['PUT'])
def update_player_expectation(sport_id, season_id, team_id, player_id, expectation_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/players/{player_id}/expectations/{expectation_id}', methods=['DELETE'])
def delete_player_expectation(sport_id, season_id, team_id, player_id, expectation_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules', methods=["POST"])
def create_schedule(sport_id, season_id, team_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules')
def get_all_schedules(sport_id, season_id, team_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}')
def get_schedule_by_id(sport_id, season_id, team_id, schedule_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}', methods=['PUT'])
def update_schedule(sport_id, season_id, team_id, schedule_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}', methods=['DELETE'])
def delete_schedule(sport_id, season_id, team_id, schedule_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games', methods=["POST"])
def create_game(sport_id, season_id, team_id, schedule_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games')
def get_all_games(sport_id, season_id, team_id, schedule_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}')
def get_game_by_id(sport_id, season_id, team_id, schedule_id, game_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}', methods=['PUT'])
def update_game(sport_id, season_id, team_id, schedule_id, game_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}', methods=['DELETE'])
def delete_game(sport_id, season_id, team_id, schedule_id, game_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/expectations', methods=["POST"])
def create_game_expectation(sport_id, season_id, team_id, schedule_id, game_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/expectations')
def get_all_game_expectations(sport_id, season_id, team_id, schedule_id, game_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/expectations/{expectation_id}')
def get_game_expectation_by_id(sport_id, season_id, team_id, schedule_id, game_id, expectation_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/expectations/{expectation_id}', methods=['PUT'])
def update_game_expectation(sport_id, season_id, team_id, schedule_id, game_id, expectation_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/expectations/{expectation_id}', methods=['DELETE'])
def delete_game_expectation(sport_id, season_id, team_id, schedule_id, game_id, expectation_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/weather_reports', methods=["POST"])
def create_weather_report(sport_id, season_id, team_id, schedule_id, game_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/weather_reports')
def get_all_weather_reports(sport_id, season_id, team_id, schedule_id, game_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/weather_reports/{weather_report_id}')
def get_weather_report_by_id(sport_id, season_id, team_id, schedule_id, game_id, weather_report_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/weather_reports/{weather_report_id}', methods=['PUT'])
def update_weather_report(sport_id, season_id, team_id, schedule_id, game_id, weather_report_id):
    pass

@app.route('/sports/{sport_id}/seasons/{season_id}/teams/{team_id}/schedules/{schedule_id}/games/{game_id}/weather_reports/{weather_report_id}', methods=['DELETE'])
def delete_weather_report(sport_id, season_id, team_id, schedule_id, game_id, weather_report_id):
    pass


if __name__ == '__main__':
    logger.info(f'Booting up the Sports API....')
    app.run(host='0.0.0.0', port=5000)

    logger.info(f'Successfully deployed the Sports API')