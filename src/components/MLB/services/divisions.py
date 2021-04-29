from utils.exceptions import Error
from components.MLB.models.divisions import DivisionModel


def create_division(conference_id, name):
    division_model = DivisionModel.create_division(conference_id=conference_id,
                                                   name=name)

    return division_model


def get_division_by_id(division_id, return_as_model=False):
    division_model = DivisionModel.get_division_by_id(division_id=division_id, return_as_model=return_as_model)

    if division_model is None:
        return Error.RESOURCE_NOT_FOUND

    return division_model if return_as_model else division_model.as_dict()


def get_all_divisions(**filters):
    division_models = DivisionModel.get_all_divisions(**filters)

    if division_models:
        return division_models

    return Error.EMPTY_SET


def update_division(division_id, conference_id=None, name=None):
    division_model = DivisionModel.get_division_by_id(division_id=division_id, return_as_model=True)

    if division_model is None:
        return Error.RESOURCE_NOT_FOUND

    return DivisionModel.update_division(division_model, conference_id=conference_id, name=name)


def delete_division(division_id):
    division_model = DivisionModel.delete_division(division_id=division_id)

    if division_model is None:
        return Error.RESOURCE_NOT_FOUND

    return division_model
