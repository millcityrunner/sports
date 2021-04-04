from utils.database import mlbdb
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class SeasonModel(mlbdb.Model):
    __tablename__ = 'seasons'
    season_id = mlbdb.Column(UUID(as_uuid=True), primary_key=True)
    season_start_date = mlbdb.Column(mlbdb.String, unique=False, nullable=False)
    season_end_date = mlbdb.Column(mlbdb.String, unique=False, nullable=False)
    champion_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'))
    runnerup_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'))

    def as_dict(self):
        return {
            'season_id': self.season_id,
            'season_start_date': self.season_start_date,
            'season_end_date': self.season_end_date,
            'champion_id': self.champion_id,
            'runnerup_id': self.runnerup_id
        }

    @staticmethod
    def get_all_seasons(**filters):
        return_as_model = False

        if filters.get('return_as_model', None) is not None:
            return_as_model = filters.get('return_as_model', False)
            del filters['return_as_model']

        return SeasonModel.query.filter_by(filters).all() if return_as_model is False else [season_model.as_dict() for season_model in SeasonModel.query.filter_by(filters).all()]

    @staticmethod
    def get_season_by_id(season_id, return_as_model=False):
        season_model = SeasonModel.query.filter_by(season_id=season_id).first()

        if return_as_model is False:
            return season_model.as_dict() if season_model else None

        else:
            return season_model if season_model else None

    @staticmethod
    def update_season(season_id, season_start_date=None, season_end_date=None, champion_id=None, runnerup_id=None,
                      return_as_model=False):
        season_model = SeasonModel.get_season_by_id(season_id=season_id, return_as_model=True)

        if season_model:
            if season_start_date is not None:
                season_model.season_start_date = season_start_date

            if season_end_date is not None:
                season_model.season_end_date = season_end_date

            if champion_id is not None:
                season_model.champion_id = champion_id

            if runnerup_id is not None:
                season_model.runnerup_id = runnerup_id

            if season_id is not None:
                season_model.season_id = season_id

            season_model.commit()
            return season_model if return_as_model else season_model.as_dict()

        return None

    @staticmethod
    def create_season(season_start_date, season_end_date, champion_id, runnerup_id):
        season_models = SeasonModel.get_all_seasons(season_start_date=season_start_date,
                                                    season_end_date=season_end_date)

        if season_models:
            return [season_model.as_dict() for season_model in season_models]

        season_id = str(uuid4())
        season_model = SeasonModel(season_id=season_id, season_start_date=season_start_date,
                                   season_end_date=season_end_date, champion_id=champion_id,
                                   runnerup_id=runnerup_id)

        mlbdb.add(season_model)
        mlbdb.commit()

        return season_model.as_dict()

    @staticmethod
    def delete_season(season_id):
        season_model = SeasonModel.get_season_by_id(season_id=season_id, return_as_model=True)

        if season_model:
            mlbdb.delete(season_model)
            mlbdb.commit()

            return season_model.as_dict()

        return None

