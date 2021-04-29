from utils.database import mlbdb
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid


class ConferenceModel(mlbdb.Model):
    __tablename__ = 'conferences'
    conference_id = mlbdb.Column(UUID(as_uuid=True), primary_key=True)
    season_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('seasons.season_id'), nullable=False)
    name = mlbdb.Column(mlbdb.String(255), nullable=False)

    def as_dict(self):
        return {
            'conference_id': self.conference_id if isinstance(self.conference_id, str) else str(self.conference_id),
            'season_id': self.season_id if isinstance(self.season_id, str) else str(self.season_id),
            'name': self.name
        }

    @staticmethod
    def create_conference(season_id, name):
        conference_model = ConferenceModel.get_all_conferences(season_id=season_id, name=name)
        if conference_model is not None:
            return conference_model[0].as_dict()

        conference_id = str(uuid.uuid4())

        conference_model = ConferenceModel(conference_id=conference_id,
                                           season_id=season_id,
                                           name=name)
        mlbdb.session.add(conference_model)
        mlbdb.session.commit()

        return conference_model.as_dict()

    @staticmethod
    def get_conference_by_id(conference_id, return_as_model=False):
        conference_model = ConferenceModel.query.filter_by(conference_id=conference_id).first()

        if conference_model:
            return conference_model if return_as_model else conference_model.as_dict()

        return None

    @staticmethod
    def get_all_conferences(**filters):
        if filters.get('return_as_model', None) is not None:
            return_as_model = filters['return_as_model']
            del filters['return_as_model']

        else:
            return_as_model = False

        conference_models = ConferenceModel.query.filter_by(**filters).all()

        if conference_models:
            return [conference_model for conference_model in conference_models] if return_as_model else [conference_model.as_dict() for
                                                                                          conference_model in conference_models]

        return None

    @staticmethod
    def update_conference(conference_model, name=None):
        if name is not None:
            conference_model.name = name
            mlbdb.commit()

        return conference_model.as_dict()

    @staticmethod
    def delete_conference(conference_id):
        conference_model = ConferenceModel.get_conference_by_id(conference_id=conference_id, return_as_model=True)

        if conference_model:
            mlbdb.delete(conference_model)
            mlbdb.commit()

            return conference_model.as_dict()

        return None
