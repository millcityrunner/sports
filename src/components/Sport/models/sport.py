from utils.database import sportdb
from sqlalchemy.dialects.postgresql import UUID


class SportModel(sportdb.Model):
    __tablename__ = 'sports'
    sport_id = sportdb.Column(UUID(as_uuid=True), primary_key=True)
    name = sportdb.Column(sportdb.String, unique=True, nullable=False)

    def as_dict(self):
        return {
            'sport_id': self.sport_id,
            'name': self.name
        }

    @staticmethod
    def create_sport(name):
        sport_model = SportModel.get_all_sports(name=name)
        if sport_model is not None:
            return sport_model[0].as_dict()

        sport_model = SportModel(name=name)
        sportdb.add(sport_model)
        sportdb.commit()

        return sport_model.as_dict()

    @staticmethod
    def get_sport_by_id(sport_id, return_as_model=False):
        sport_model = SportModel.query.filter_by(sport_id=sport_id).first()

        if sport_model:
            return sport_model if return_as_model else sport_model.as_dict()

        return None

    @staticmethod
    def get_all_sports(**filters):
        if filters.get('return_as_model', None) is not None:
            return_as_model = filters['return_as_model']
            del filters['return_as_model']

        else:
            return_as_model = False

        sport_models = SportModel.query.filter_by(filters).all()

        if sport_models:
            return [sport_model for sport_model in sport_models] if return_as_model else [sport_model.as_dict() for sport_model in sport_models]

        return None

    @staticmethod
    def update_sport(sport_id, name=None):
        sport_model = SportModel.get_sport_by_id(sport_id=sport_id, return_as_model=True)

        if sport_model:
            if name is not None:
                sport_model.name = name

            sportdb.commit()
            return sport_model.as_dict()

        return None

    @staticmethod
    def delete_sport(sport_id):
        sport_model = SportModel.get_sport_by_id(sport_id=sport_id, return_as_model=True)

        if sport_model:
            sportdb.delete(sport_model)
            sportdb.commit()

            return sport_model.as_dict()

        return None
