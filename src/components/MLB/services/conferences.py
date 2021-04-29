from utils.exceptions import Error
from components.MLB.models.conferences import ConferenceModel


def create_conference(season_id, name):
    conference_model = ConferenceModel.create_conference(season_id=season_id,
                                                         name=name)

    return conference_model


def get_conference_by_id(conference_id, return_as_model=False):
    conference_model = ConferenceModel.get_conference_by_id(conference_id=conference_id, return_as_model=return_as_model)

    if conference_model is None:
        return Error.RESOURCE_NOT_FOUND

    return conference_model if return_as_model else conference_model.as_dict()


def get_all_conferences(**filters):
    conference_models = ConferenceModel.get_all_conferences(**filters)

    if conference_models:
        return conference_models

    return Error.EMPTY_SET


def update_conference(conference_id, name=None):
    conference_model = ConferenceModel.get_conference_by_id(conference_id=conference_id, return_as_model=True)

    if conference_model is None:
        return Error.RESOURCE_NOT_FOUND

    return ConferenceModel.update_conference(conference_model, name=name)


def delete_conference(conference_id):
    conference_model = ConferenceModel.delete_conference(conference_id=conference_id)

    if conference_model is None:
        return Error.RESOURCE_NOT_FOUND

    return conference_model
