from components.Sports.models import SportModel

from utils.exceptions import Error


def create_sport(req_data):
    name = req_data.__getattribute__('name') if req_data.__contains__('name') else None

    sport_model = SportModel.create_sport(name)

    if sport_model:
        return sport_model

    return Error.INVALID_VALUE
