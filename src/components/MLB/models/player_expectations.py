from utils.database import mlbdb
from sqlalchemy.dialects.postgresql import UUID, JSON
from uuid import uuid4


class PlayerExpectationModel(mlbdb.Model):
    __tablename__ = 'player_expectations'
    player_expectation_id = mlbdb.Column(UUID(as_uuid=True), primary_key=True)
    date = mlbdb.Column(mlbdb.String, unique=False, nullable=False)
    hits = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    doubles = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    triples = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    homeruns = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    at_bats = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    runs = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    earned_runs = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    batter_walks = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    strikeouts = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    hit_by_pitches = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    sacrifice_hits = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    sacrifice_flies = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    stolen_bases = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    errors = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    grounded_into_dp = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    left_on_base = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    runners_in_scoring_position = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    runs_batted_in = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    pitches_thrown = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    strikes_thrown = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    balls_thrown = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    wild_pitches = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    strikeouts_thrown = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    innings_pitched = mlbdb.Column(mlbdb.Float, unique=False, nullable=False)
    batting_order_position = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    dome = mlbdb.Column(mlbdb.Boolean, unique=False, nullable=False)
    game_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('games.game_id'), nullable=False)
    weather_report_id = mlbdb.Column(UUID(as_uuid=True),
                                     mlbdb.ForeignKey('weather_report_id.weather_report_id'), nullable=False)
    player_team_id = mlbdb.Column(UUID(as_uuid=True),
                                  mlbdb.ForeignKey('teams.team_id'), nullable=False)
    opponent_team_id = mlbdb.Column(UUID(as_uuid=True),
                                    mlbdb.ForeignKey('teams.teams_id'), nullable=False)

    def as_dict(self):
        return {
            'player_expectation_id': self.player_expectation_id,
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
    def get_all_player_expectations(**filters):
        return_as_model = False

        if filters.get('return_as_model', None) is not None:
            return_as_model = filters.get('return_as_model', False)
            del filters['return_as_model']

        return PlayerExpectationModel.query.filter_by(filters).all() if return_as_model is False else [player_expectation_model.as_dict() for player_expectation_model in PlayerExpectationModel.query.filter_by(filters).all()]

    @staticmethod
    def get_player_expectation_by_id(player_expectation_id, return_as_model=False):
        player_expectation_model = PlayerExpectationModel.query.filter_by(player_expectation_id=player_expectation_id).first()

        if return_as_model is False:
            return player_expectation_model.as_dict() if player_expectation_model else None

        else:
            return player_expectation_model if player_expectation_model else None

    @staticmethod
    def update_player_expectation(player_expectation_id, away_team_id, home_team_id, winner_id, loser_id,
                                  winner_score, loser_score, winning_pitcher_id, losing_pitcher_id,
                                  date, return_as_model=False):
        player_expectation_model = PlayerExpectationModel.get_player_expectation_by_id(player_expectation_id=player_expectation_id,
                                                                                       return_as_model=True)

        if player_expectation_model:
            if away_team_id is not None:
                player_expectation_model.away_team_id = away_team_id

            if home_team_id is not None:
                player_expectation_model.home_team_id = home_team_id

            if winner_id is not None:
                player_expectation_model.winner_id = winner_id

            if loser_id is not None:
                player_expectation_model.loser_id = loser_id

            if winner_score is not None:
                player_expectation_model.winner_score = winner_score

            if loser_score is not None:
                player_expectation_model.loser_score = loser_score

            if winning_pitcher_id is not None:
                player_expectation_model.winning_pitcher_id = winning_pitcher_id

            if losing_pitcher_id is not None:
                player_expectation_model.losing_pitcher_id = losing_pitcher_id

            if date is not None:
                player_expectation_model.date = date

            player_expectation_model.commit()
            return player_expectation_model if return_as_model else player_expectation_model.as_dict()

        return None

    @staticmethod
    def create_player_expectation(away_team_id, home_team_id, winner_id, loser_id, winner_score, loser_score,
                                  winning_pitcher_id, losing_pitcher_id, date):
        player_expectation_models = PlayerExpectationModel.get_all_player_expectations(away_team_id=away_team_id,
                                                                                       home_team_id=home_team_id,
                                                                                       winner_id=winner_id,
                                                                                       loser_id=loser_id,
                                                                                       winner_score=winner_score,
                                                                                       loser_score=loser_score,
                                                                                       winning_pitcher_id=winning_pitcher_id,
                                                                                       losing_pitcher_id=losing_pitcher_id,
                                                                                       date=date)

        if player_expectation_models:
            return [player_expectation_model.as_dict() for player_expectation_model in player_expectation_models]

        player_expectation_id = str(uuid4())
        player_expectation_model = PlayerExpectationModel(player_expectation_id=player_expectation_id,
                                                          away_team_id=away_team_id,
                                                          home_team_id=home_team_id,
                                                          winner_id=winner_id,
                                                          loser_id=loser_id,
                                                          winner_score=winner_score,
                                                          loser_score=loser_score,
                                                          winning_pitcher_id=winning_pitcher_id,
                                                          losing_pitcher_id=losing_pitcher_id,
                                                          date=date)

        mlbdb.add(player_expectation_model)
        mlbdb.commit()

        return player_expectation_model.as_dict()

    @staticmethod
    def delete_expectation(player_expectation_id):
        player_expectation_model = PlayerExpectationModel.get_player_expectation_by_id(player_expectation_id=player_expectation_id,
                                                                                       return_as_model=True)

        if player_expectation_model:
            mlbdb.delete(player_expectation_model)
            mlbdb.commit()

            return player_expectation_model.as_dict()

        return None

