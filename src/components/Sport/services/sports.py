from components.Sport.models.sport import SportModel
from utils.exceptions import Error


def create_sport(name):
    sport_model = SportModel.create_sport(name=name)

    if sport_model:
        return sport_model

    return Error.INVALID_VALUE
