from utils.database import mlbdb
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class TeamModel(mlbdb.Model):
    __tablename__ = 'teams'
    team_id = mlbdb.Column(UUID(as_uuid=True), primary_key=True)
    season_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('seasons.season_id'))
    team_name = mlbdb.Column(mlbdb.String, unique=False, nullable=False)
    team_city = mlbdb.Column(mlbdb.String, unique=False, nullable=False)
    conference_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('conferences.conference_id'))
    division_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('divisions.division_id'))

    def as_dict(self):
        return {
            'team_id': self.team_id,
            'team_name': self.team_name,
            'team_city': self.team_city,
            'season_id': self.season_id,
            'conference_id': self.conference_id,
            'division_id': self.division_id
        }

    @staticmethod
    def get_all_teams(**filters):
        return_as_model = False

        if filters.get('return_as_model', None) is not None:
            return_as_model = filters.get('return_as_model', False)
            del filters['return_as_model']

        return TeamModel.query.filter_by(filters).all() if return_as_model is False else [team_model.as_dict() for team_model in TeamModel.query.filter_by(filters).all()]

    @staticmethod
    def get_team_by_id(team_id, return_as_model=False):
        team_model = TeamModel.query.filter_by(team_id=team_id).first()

        if return_as_model is False:
            return team_model.as_dict() if team_model else None

        else:
            return team_model if team_model else None

    @staticmethod
    def update_team(team_id, team_name=None, team_city=None, conference_id=None, division_id=None, season_id=None,
                      return_as_model=False):
        team_model = TeamModel.get_team_by_id(team_id=team_id, return_as_model=True)

        if team_model:
            if team_name is not None:
                team_model.team_name = team_name

            if team_city is not None:
                team_model.team_city = team_city

            if conference_id is not None:
                team_model.conference_id = conference_id

            if division_id is not None:
                team_model.division_id = division_id

            if season_id is not None:
                team_model.season_id = season_id

            team_model.commit()
            return team_model if return_as_model else team_model.as_dict()

        return None

    @staticmethod
    def create_team(team_name, team_city, conference_id, division_id, season_id):
        team_models = TeamModel.get_all_teams(team_name=team_name,
                                              team_city=team_city,
                                              season_id=season_id)

        if team_models:
            return [team_model.as_dict() for team_model in team_models]

        team_id = str(uuid4())
        team_model = TeamModel(team_id=team_id, team_name=team_name, team_city=team_city,
                               conference_id=conference_id, division_id=division_id, season_id=season_id)

        mlbdb.add(team_model)
        mlbdb.commit()

        return team_model.as_dict()

    @staticmethod
    def delete_team(team_id):
        team_model = TeamModel.get_team_by_id(team_id=team_id, return_as_model=True)

        if team_model:
            mlbdb.delete(team_model)
            mlbdb.commit()

            return team_model.as_dict()

        return None

