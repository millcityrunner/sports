from utils.database import mlbdb
from sqlalchemy.dialects.postgresql import UUID, JSON
from uuid import uuid4


class GameExpectationModel(mlbdb.Model):
    __tablename__ = 'game_expectations'
    game_expectation_id = mlbdb.Column(UUID(as_uuid=True), primary_key=True)
    away_team_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'), nullable=False)
    home_team_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'), nullable=False)
    winner_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'), nullable=False)
    loser_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'), nullable=False)
    winner_score = mlbdb.Column(mlbdb.Integer, nullable=False)
    loser_score = mlbdb.Column(mlbdb.Integer, nullable=False)
    winning_pitcher_id = mlbdb.Column(UUID(as_uuid=True), nullable=False)
    losing_pitcher_id = mlbdb.Column(UUID(as_uuid=True), nullable=False)
    game_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('games.game_id'), nullable=False),
    date = mlbdb.Column(mlbdb.String, nullable=False)

    def as_dict(self):
        return {
            'game_expectation_id': self.game_expectation_id,
            'away_team_id': self.away_team_id,
            'home_team_id': self.home_team_id,
            'winner_id': self.winner_id,
            'loser_id': self.loser_id,
            'winner_score': self.winner_score,
            'loser_score': self.loser_score,
            'winning_pitcher_id': self.winning_pitcher_id,
            'losing_pitcher_id': self.losing_pitcher_id,
            'game_id': self.game_id,
            'date': self.date
        }

    @staticmethod
    def get_all_expectations(**filters):
        return_as_model = False

        if filters.get('return_as_model', None) is not None:
            return_as_model = filters.get('return_as_model', False)
            del filters['return_as_model']

        return GameExpectationModel.query.filter_by(filters).all() if return_as_model is False else [expectation_model.as_dict() for expectation_model in GameExpectationModel.query.filter_by(filters).all()]

    @staticmethod
    def get_game_expectation_by_id(game_expectation_id, return_as_model=False):
        game_expectation_model = GameExpectationModel.query.filter_by(game_expectation_id=game_expectation_id).first()

        if return_as_model is False:
            return game_expectation_model.as_dict() if game_expectation_model else None

        else:
            return game_expectation_model if game_expectation_model else None

    @staticmethod
    def update_expectation(game_expectation_id, away_team_id, home_team_id, winner_id, loser_id,
                           winner_score, loser_score, winning_pitcher_id, losing_pitcher_id, game_id,
                           date, return_as_model=False):
        game_expectation_model = GameExpectationModel.get_game_expectation_by_id(game_expectation_id=game_expectation_id,
                                                                                 return_as_model=True)

        if game_expectation_model:
            if away_team_id is not None:
                game_expectation_model.away_team_id = away_team_id

            if home_team_id is not None:
                game_expectation_model.home_team_id = home_team_id

            if winner_id is not None:
                game_expectation_model.winner_id = winner_id

            if loser_id is not None:
                game_expectation_model.loser_id = loser_id

            if winner_score is not None:
                game_expectation_model.winner_score = winner_score

            if loser_score is not None:
                game_expectation_model.loser_score = loser_score

            if winning_pitcher_id is not None:
                game_expectation_model.winning_pitcher_id = winning_pitcher_id

            if losing_pitcher_id is not None:
                game_expectation_model.losing_pitcher_id = losing_pitcher_id

            if game_id is not None:
                game_expectation_model.game_id = game_id

            if date is not None:
                game_expectation_model.date = date

            game_expectation_model.commit()
            return game_expectation_model if return_as_model else game_expectation_model.as_dict()

        return None

    @staticmethod
    def create_game_expectation(away_team_id, home_team_id, winner_id, loser_id, winner_score, loser_score,
                                winning_pitcher_id, losing_pitcher_id, game_id, date):
        game_expectation_models = GameExpectationModel.get_all_game_expectations(away_team_id=away_team_id,
                                                                                 home_team_id=home_team_id,
                                                                                 winner_id=winner_id,
                                                                                 loser_id=loser_id,
                                                                                 winner_score=winner_score,
                                                                                 loser_score=loser_score,
                                                                                 winning_pitcher_id=winning_pitcher_id,
                                                                                 losing_pitcher_id=losing_pitcher_id,
                                                                                 game_id=game_id,
                                                                                 date=date)

        if game_expectation_models:
            return [game_expectation_model.as_dict() for game_expectation_model in game_expectation_models]

        game_expectation_id = str(uuid4())
        game_expectation_model = GameExpectationModel(game_expectation_id=game_expectation_id,
                                                      away_team_id=away_team_id,
                                                      home_team_id=home_team_id,
                                                      winner_id=winner_id,
                                                      loser_id=loser_id,
                                                      winner_score=winner_score,
                                                      loser_score=loser_score,
                                                      winning_pitcher_id=winning_pitcher_id,
                                                      losing_pitcher_id=losing_pitcher_id,
                                                      game_id=game_id,
                                                      date=date)

        mlbdb.add(game_expectation_model)
        mlbdb.commit()

        return game_expectation_model.as_dict()

    @staticmethod
    def delete_expectation(game_expectation_id):
        game_expectation_model = GameExpectationModel.get_game_expectation_by_id(game_expectation_id=game_expectation_id,
                                                                                 return_as_model=True)

        if game_expectation_model:
            mlbdb.delete(game_expectation_model)
            mlbdb.commit()

            return game_expectation_model.as_dict()

        return None

