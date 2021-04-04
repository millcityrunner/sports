from utils.database import mlbdb
from sqlalchemy.dialects.postgresql import UUID, JSON
from uuid import uuid4


class ExpectationModel(mlbdb.Model):
    __tablename__ = 'expectations'
    expectation_id = mlbdb.Column(UUID(as_uuid=True), primary_key=True)
    away_team_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'), nullable=False)
    home_team_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'), nullable=False)
    winner_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'), nullable=False)
    loser_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'), nullable=False)
    winner_score = mlbdb.Column(mlbdb.Integer, nullable=False)
    loser_score = mlbdb.Column(mlbdb.Integer, nullable=False)
    winning_pitcher_id = mlbdb.Column(UUID(as_uuid=True), nullable=False)
    losing_pitcher_id = mlbdb.Column(UUID(as_uuid=True), nullable=False)
    date = mlbdb.Column(mlbdb.String, nullable=False)

    def as_dict(self):
        return {
            'expectation_id': self.expectation_id,
            'away_team_id': self.away_team_id,
            'home_team_id': self.home_team_id,
            'winner_id': self.winner_id,
            'loser_id': self.loser_id,
            'winner_score': self.winner_score,
            'loser_score': self.loser_score,
            'winning_pitcher_id': self.winning_pitcher_id,
            'losing_pitcher_id': self.losing_pitcher_id,
            'date': self.date
        }

    @staticmethod
    def get_all_expectations(**filters):
        return_as_model = False

        if filters.get('return_as_model', None) is not None:
            return_as_model = filters.get('return_as_model', False)
            del filters['return_as_model']

        return ExpectationModel.query.filter_by(filters).all() if return_as_model is False else [expectation_model.as_dict() for expectation_model in ExpectationModel.query.filter_by(filters).all()]

    @staticmethod
    def get_expectation_by_id(expectation_id, return_as_model=False):
        expectation_model = ExpectationModel.query.filter_by(expectation_id=expectation_id).first()

        if return_as_model is False:
            return expectation_model.as_dict() if expectation_model else None

        else:
            return expectation_model if expectation_model else None

    @staticmethod
    def update_expectation(expectation_id, away_team_id, home_team_id, winner_id, loser_id,
                           winner_score, loser_score, winning_pitcher_id, losing_pitcher_id,
                           date, return_as_model=False):
        expectation_model = ExpectationModel.get_expectation_by_id(expectation_id=expectation_id,
                                                                   return_as_model=True)

        if expectation_model:
            if away_team_id is not None:
                expectation_model.away_team_id = away_team_id

            if home_team_id is not None:
                expectation_model.home_team_id = home_team_id

            if winner_id is not None:
                expectation_model.winner_id = winner_id

            if loser_id is not None:
                expectation_model.loser_id = loser_id

            if winner_score is not None:
                expectation_model.winner_score = winner_score

            if loser_score is not None:
                expectation_model.loser_score = loser_score

            if winning_pitcher_id is not None:
                expectation_model.winning_pitcher_id = winning_pitcher_id

            if losing_pitcher_id is not None:
                expectation_model.losing_pitcher_id = losing_pitcher_id

            if date is not None:
                expectation_model.date = date

            expectation_model.commit()
            return expectation_model if return_as_model else expectation_model.as_dict()

        return None

    @staticmethod
    def create_expectation(away_team_id, home_team_id, winner_id, loser_id, winner_score, loser_score,
                           winning_pitcher_id, losing_pitcher_id, date):
        expectation_models = ExpectationModel.get_all_expectations(away_team_id=away_team_id,
                                                                   home_team_id=home_team_id,
                                                                   winner_id=winner_id,
                                                                   loser_id=loser_id,
                                                                   winner_score=winner_score,
                                                                   loser_score=loser_score,
                                                                   winning_pitcher_id=winning_pitcher_id,
                                                                   losing_pitcher_id=losing_pitcher_id,
                                                                   date=date)

        if expectation_models:
            return [expectation_model.as_dict() for expectation_model in expectation_models]

        expectation_id = str(uuid4())
        expectation_model = ExpectationModel(expectation_id=expectation_id,
                                             away_team_id=away_team_id,
                                             home_team_id=home_team_id,
                                             winner_id=winner_id,
                                             loser_id=loser_id,
                                             winner_score=winner_score,
                                             loser_score=loser_score,
                                             winning_pitcher_id=winning_pitcher_id,
                                             losing_pitcher_id=losing_pitcher_id,
                                             date=date)

        mlbdb.add(expectation_model)
        mlbdb.commit()

        return expectation_model.as_dict()

    @staticmethod
    def delete_expectation(expectation_id):
        expectation_model = ExpectationModel.get_expectation_by_id(expectation_id=expectation_id, return_as_model=True)

        if expectation_model:
            mlbdb.delete(expectation_model)
            mlbdb.commit()

            return expectation_model.as_dict()

        return None

