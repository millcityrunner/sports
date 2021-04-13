from utils.exceptions import Error
from components.MLB.models.seasons import SeasonModel


def create_season(sport_id, season_start_date, season_end_date, champion_id, runnerup_id):
    season_model = SeasonModel.create_season(sport_id=sport_id,
                                             season_start_date=season_start_date,
                                             season_end_date=season_end_date,
                                             champion_id=champion_id,
                                             runnerup_id=runnerup_id)

    return season_model


def get_season_by_id(season_id, return_as_model=False):
    season_model = SeasonModel.get_season_by_id(season_id=season_id, return_as_model=return_as_model)

    if season_model is None:
        return Error.RESOURCE_NOT_FOUND

    return season_model if return_as_model else season_model.as_dict()


def get_all_seasons(**filters):
    season_models = SeasonModel.get_all_seasons(**filters)

    if season_models:
        return season_models

    return Error.EMPTY_SET


def update_season(season_id, sport_id=None, season_start_date=None, season_end_date=None, champion_id=None,
                  runnerup_id=None,
                  return_as_model=False):
    season_model = SeasonModel.get_season_by_id(season_id=season_id, return_as_model=True)

    if season_model is None:
        return Error.RESOURCE_NOT_FOUND

    return SeasonModel.update_season(season_model, sport_id=sport_id,
                                     season_start_date=season_start_date,
                                     season_end_date=season_end_date,
                                     champion_id=champion_id, runnerup_id=runnerup_id,
                                     return_as_model=return_as_model)


def delete_season(season_id):
    season_model = SeasonModel.delete_season(season_id=season_id)

    if season_model is None:
        return Error.RESOURCE_NOT_FOUND

    return season_model
