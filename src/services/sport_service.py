from components.Sport.models.sport import SportModel

from components.Sport.serializers.CreateSportRequestData import CreateSportRequestData
from components.Sport.serializers.UpdateSportRequestData import UpdateSportRequestData

from utils.exceptions import Error


def create_sport(request_body):
    try:
        req_data = CreateSportRequestData(data=request_body)
        name = req_data.name

    except (ValueError, AttributeError, KeyError) as e:
        return Error.INVALID_VALUE

    sport_model = SportModel.create_sport(name)

    if sport_model:
        return sport_model

    return Error.INVALID_VALUE


def get_all_sports(**filters):
    sport_models = SportModel.get_all_sports(**filters)

    return sport_models if sport_models else Error.EMPTY_SET


def get_sport_by_id(sport_id=None, return_as_model=False):
    if sport_id is None:
        return Error.INVALID_VALUE

    sport_model = SportModel.get_sport_by_id(sport_id=sport_id, return_as_model=return_as_model)

    return sport_model if sport_model is not None else Error.RESOURCE_NOT_FOUND


def update_sport(sport_id=None, request_body=None):
    try:
        req_data = UpdateSportRequestData(data=request_body)

    except:
        return Error.INVALID_VALUE

    name = request_body.get('name', None)

    if sport_id is None or name is None:
        return Error.INVALID_VALUE

    sport_model = SportModel.update_sport(sport_id=sport_id, name=name)

    return sport_model if sport_model is not None else Error.RESOURCE_NOT_FOUND


def delete_sport(sport_id=None):
    if sport_id is None:
        return Error.INVALID_VALUE

    sport_model = SportModel.delete_sport(sport_id=sport_id)

    return sport_model if sport_model else Error.RESOURCE_NOT_FOUND
