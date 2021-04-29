from utils.database import mlbdb
from sqlalchemy.dialects.postgresql import UUID, JSON
from uuid import uuid4


class InjuryReportModel(mlbdb.Model):
    __tablename__ = 'injury_reports'
    injury_report_id = mlbdb.Column(UUID(as_uuid=True), primary_key=True)
    team_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'), nullable=False)
    players = mlbdb.Column(JSON, nullable=True)
    date = mlbdb.Column(mlbdb.String, nullable=False)

    def as_dict(self):
        return {
            'injury_report_id': self.injury_report_id,
            'team_id': self.team_id,
            'players': self.players,
            'date': self.date
        }

    @staticmethod
    def get_all_injury_reports(**filters):
        return_as_model = False

        if filters.get('return_as_model', None) is not None:
            return_as_model = filters.get('return_as_model', False)
            del filters['return_as_model']

        return InjuryReportModel.query.filter_by(filters).all() if return_as_model is False else [injury_report_model.as_dict() for injury_report_model in InjuryReportModel.query.filter_by(filters).all()]

    @staticmethod
    def get_injury_report_by_id(injury_report_id, return_as_model=False):
        injury_report_model = InjuryReportModel.query.filter_by(injury_report_id=injury_report_id).first()

        if return_as_model is False:
            return injury_report_model.as_dict() if injury_report_model else None

        else:
            return injury_report_model if injury_report_model else None

    @staticmethod
    def update_injury_report(injury_report_id, team_id, players, date, return_as_model=False):
        injury_report_model = InjuryReportModel.get_injury_report_by_id(injury_report_id=injury_report_id,
                                                                        return_as_model=True)

        if injury_report_model:
            if team_id is not None:
                injury_report_model.team_id = team_id

            if players is not None:
                injury_report_model.players = players

            if date is not None:
                injury_report_model.date = date

            injury_report_model.commit()
            return injury_report_model if return_as_model else injury_report_model.as_dict()

        return None

    @staticmethod
    def create_injury_report(team_id, players, date):
        injury_report_models = InjuryReportModel.get_all_injury_reports(team_id=team_id, players=players, date=date)

        if injury_report_models:
            return [injury_report_model.as_dict() for injury_report_model in injury_report_models]

        injury_report_id = str(uuid4())
        injury_report_model = InjuryReportModel(injury_report_id=injury_report_id, team_id=team_id,
                                                players=players, date=date)

        mlbdb.add(injury_report_model)
        mlbdb.commit()

        return injury_report_model.as_dict()

    @staticmethod
    def delete_injury_report(injury_report_id):
        injury_report_model = InjuryReportModel.get_injury_report_by_id(injury_report_id=injury_report_id,
                                                                        return_as_model=True)

        if injury_report_model:
            mlbdb.delete(injury_report_model)
            mlbdb.commit()

            return injury_report_model.as_dict()

        return None

