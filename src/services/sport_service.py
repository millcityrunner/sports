from components.Sport.models.sport import SportModel

from utils.exceptions import Error


def create_sport(req_data):
    name = req_data.__getattribute__('name') if req_data.__dict__.get('name') else None

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


def update_sport(sport_id=None, name=None):
    if sport_id is None or name is None:
        return Error.INVALID_VALUE

    sport_model = SportModel.update_sport(sport_id=sport_id, name=name)

    return sport_model if sport_model is not None else Error.RESOURCE_NOT_FOUND


def delete_sport(sport_id=None):
    if sport_id is None:
        return Error.INVALID_VALUE

    sport_model = SportModel.delete_sport(sport_id=sport_id)

    return sport_model if sport_model else Error.RESOURCE_NOT_FOUND
