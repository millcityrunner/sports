from utils.database import mlbdb
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid


class DivisionModel(mlbdb.Model):
    __tablename__ = 'divisions'
    division_id = mlbdb.Column(UUID(as_uuid=True), primary_key=True)
    conference_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('conferences.conference_id'))
    name = mlbdb.Column(mlbdb.String(255), nullable=False)

    def as_dict(self):
        return {
            'division_id': self.division_id if isinstance(self.division_id, str) else str(self.division_id),
            'conference_id': self.conference_id if isinstance(self.conference_id, str) else str(self.conference_id),
            'name': self.name
        }

    @staticmethod
    def create_division(conference_id, name):
        division_model = DivisionModel.get_all_divisions(conference_id=conference_id, name=name)
        if division_model is not None:
            return division_model[0].as_dict()

        division_id = str(uuid.uuid4())

        division_model = DivisionModel(division_id=division_id,
                                       conference_id=conference_id,
                                       name=name)
        mlbdb.session.add(division_model)
        mlbdb.session.commit()

        return division_model.as_dict()

    @staticmethod
    def get_division_by_id(division_id, return_as_model=False):
        division_model = DivisionModel.query.filter_by(division_id=division_id).first()

        if division_model:
            return division_model if return_as_model else division_model.as_dict()

        return None

    @staticmethod
    def get_all_divisions(**filters):
        if filters.get('return_as_model', None) is not None:
            return_as_model = filters['return_as_model']
            del filters['return_as_model']

        else:
            return_as_model = False

        division_models = DivisionModel.query.filter_by(**filters).all()

        if division_models:
            return [division_model for division_model in division_models] if return_as_model else [
                division_model.as_dict() for
                division_model in division_models]

        return None

    @staticmethod
    def update_division(division_id, conference_id=None, name=None):
        division_model = DivisionModel.get_division_by_id(division_id=division_id, return_as_model=True)

        if division_model:
            if conference_id is not None:
                division_model.conference_id = conference_id

            if name is not None:
                division_model.name = name

            mlbdb.commit()
            return division_model.as_dict()

        return None

    @staticmethod
    def delete_division(division_id):
        division_model = DivisionModel.get_division_by_id(division_id=division_id, return_as_model=True)

        if division_model:
            mlbdb.delete(division_model)
            mlbdb.commit()

            return division_model.as_dict()

        return None
