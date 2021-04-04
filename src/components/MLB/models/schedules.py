from utils.database import mlbdb
from sqlalchemy.dialects.postgresql import UUID, JSON
from uuid import uuid4


class ScheduleModel(mlbdb.Model):
    __tablename__ = 'schedules'
    schedule_id = mlbdb.Column(UUID(as_uuid=True), primary_key=True)
    away_team_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'), nullable=False)
    home_team_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'), nullable=False)
    game_start_time = mlbdb.Column(mlbdb.String, nullable=True)
    date = mlbdb.Column(mlbdb.String, nullable=False)

    def as_dict(self):
        return {
            'schedule_id': self.schedule_id,
            'away_team_id': self.away_team_id,
            'home_team_id': self.home_team_id,
            'game_start_time': self.game_start_time,
            'date': self.date
        }

    @staticmethod
    def get_all_schedules(**filters):
        return_as_model = False

        if filters.get('return_as_model', None) is not None:
            return_as_model = filters.get('return_as_model', False)
            del filters['return_as_model']

        return ScheduleModel.query.filter_by(filters).all() if return_as_model is False else [schedule_model.as_dict() for schedule_model in ScheduleModel.query.filter_by(filters).all()]

    @staticmethod
    def get_schedule_by_id(schedule_id, return_as_model=False):
        schedule_model = ScheduleModel.query.filter_by(schedule_id=schedule_id).first()

        if return_as_model is False:
            return schedule_model.as_dict() if schedule_model else None

        else:
            return schedule_model if schedule_model else None

    @staticmethod
    def update_schedule(schedule_id, away_team_id, home_team_id, game_start_time, date, return_as_model=False):
        schedule_model = ScheduleModel.get_schedule_by_id(schedule_id=schedule_id,
                                                          return_as_model=True)

        if schedule_model:
            if away_team_id is not None:
                schedule_model.away_team_id = away_team_id

            if home_team_id is not None:
                schedule_model.home_team_id = home_team_id

            if game_start_time is not None:
                schedule_model.game_start_time = game_start_time

            if date is not None:
                schedule_model.date = date

            schedule_model.commit()
            return schedule_model if return_as_model else schedule_model.as_dict()

        return None

    @staticmethod
    def create_schedule(away_team_id, home_team_id, game_start_time, date):
        schedule_models = ScheduleModel.get_all_schedules(away_team_id=away_team_id,
                                                          home_team_id=home_team_id,
                                                          game_start_time=game_start_time,
                                                          date=date)

        if schedule_models:
            return [schedule_model.as_dict() for schedule_model in schedule_models]

        schedule_id = str(uuid4())
        schedule_model = ScheduleModel(schedule_id=schedule_id,
                                       away_team_id=away_team_id,
                                       home_team_id=home_team_id,
                                       game_start_time=game_start_time,
                                       date=date)

        mlbdb.add(schedule_model)
        mlbdb.commit()

        return schedule_model.as_dict()

    @staticmethod
    def delete_schedule(schedule_id):
        schedule_model = ScheduleModel.get_schedule_by_id(schedule_id=schedule_id, return_as_model=True)

        if schedule_model:
            mlbdb.delete(schedule_model)
            mlbdb.commit()

            return schedule_model.as_dict()

        return None

