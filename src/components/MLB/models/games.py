from utils.database import mlbdb
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class GameModel(mlbdb.Model):
    __tablename__ = 'games'
    game_id = mlbdb.Column(UUID(as_uuid=True), primary_key=True)
    date = mlbdb.Column(mlbdb.String, unique=False, nullable=False)
    winner_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'), nullable=False)
    loser_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'), nullable=False)
    winner_score = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    loser_score = mlbdb.Column(mlbdb.Integer, unique=False, nullable=False)
    winning_pitcher_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('players.player_id'), nullable=False)
    losing_pitcher_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('players.player_id'), nullable=False)
    weather_report_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('weather_reports.weather_report_id'), nullable=False)
    expectation_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('expectations.expectation_id'), nullable=False)
    injury_reports_away_team = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('injury_reports.injury_report_id'), nullable=False)
    injury_reports_home_team = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('injury_reports.injury_report_id'), nullable=False)
    away_team_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'), nullable=False)
    home_team_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'), nullable=False)
    dome = mlbdb.Column(mlbdb.Boolean, unique=False, nullable=False)

    def as_dict(self):
        return {
            'game_id': self.game_id,
            'date': self.date,
            'dome': self.dome,
            'away_team_id': self.away_team_id,
            'home_team_id': self.home_team_id,
            'winner_id': self.winner_id,
            'loser_id': self.loser_id,
            'winner_score': self.winner_score,
            'loser_score': self.loser_score,
            'winning_pitcher_id': self.winning_pitcher_id,
            'losing_pitcher_id': self.losing_pitcher_id,
            'weather_report_id': self.weather_report_id,
            'expectation_id': self.expectation_id,
            'injury_reports_away_team': self.injury_reports_away_team,
            'injury_reports_home_team': self.injury_reports_home_team
        }

    @staticmethod
    def get_all_games(**filters):
        return_as_model = False

        if filters.get('return_as_model', None) is not None:
            return_as_model = filters.get('return_as_model', False)
            del filters['return_as_model']

        return GameModel.query.filter_by(filters).all() if return_as_model is False else [game_model.as_dict() for game_model in GameModel.query.filter_by(filters).all()]

    @staticmethod
    def get_game_by_id(game_id, return_as_model=False):
        game_model = GameModel.query.filter_by(game_id=game_id).first()

        if return_as_model is False:
            return game_model.as_dict() if game_model else None

        else:
            return game_model if game_model else None

    @staticmethod
    def update_game(game_id, date=None, dome=None, away_team_id=None, home_team_id=None, winner_id=None,
                    loser_id=None, winner_score=None, loser_score=None, winning_pitcher_id=None,
                    losing_pitcher_id=None, weather_report_id=None, expectation_id=None, injury_reports_away_team=None,
                    injury_reports_home_team=None, return_as_model=False):
        game_model = GameModel.get_game_by_id(game_id=game_id, return_as_model=True)

        if game_model:
            if date is not None:
                game_model.date = date

            if dome is not None:
                game_model.dome = dome

            if away_team_id is not None:
                game_model.away_team_id = away_team_id

            if home_team_id is not None:
                game_model.home_team_id = home_team_id

            if winner_id is not None:
                game_model.winner_id = winner_id

            if loser_id is not None:
                game_model.loser_id = loser_id

            if winner_score is not None:
                game_model.winner_score = winner_score

            if loser_score is not None:
                game_model.loser_score = loser_score

            if winning_pitcher_id is not None:
                game_model.winning_pitcher_id = winning_pitcher_id

            if losing_pitcher_id is not None:
                game_model.losing_pitcher_id = losing_pitcher_id

            if weather_report_id is not None:
                game_model.weather_report_id = weather_report_id

            if expectation_id is not None:
                game_model.expectation_id = expectation_id

            if injury_reports_home_team is not None:
                game_model.injury_reports_home_team = injury_reports_home_team

            if injury_reports_away_team is not None:
                game_model.injury_reports_away_team = injury_reports_away_team

            game_model.commit()
            return game_model if return_as_model else game_model.as_dict()

        return None

    @staticmethod
    def create_game(date, dome, away_team_id, home_team_id, winner_id,
                    loser_id, winner_score, loser_score, winning_pitcher_id,
                    losing_pitcher_id, weather_report_id, expectation_id, injury_reports_away_team,
                    injury_reports_home_team):
        game_models = GameModel.get_all_games(date=date,
                                              away_team_id=away_team_id,
                                              home_team_id=home_team_id,
                                              winner_score=winner_score,
                                              loser_score=loser_score,
                                              winner_id=winner_id,
                                              loser_id=loser_id,
                                              winning_pitcher_id=winning_pitcher_id,
                                              losing_pitcher_id=losing_pitcher_id)

        if game_models:
            return [game_model.as_dict() for game_model in game_models]

        game_id = str(uuid4())
        game_model = GameModel(game_id=game_id, date=date, dome=dome, away_team_id=away_team_id,
                               home_team_id=home_team_id, winner_id=winner_id,
                               loser_id=loser_id, winner_score=winner_score, loser_score=loser_score,
                               winning_pitcher_id=winning_pitcher_id,
                               losing_pitcher_id=losing_pitcher_id, weather_report_id=weather_report_id,
                               expectation_id=expectation_id,
                               injury_reports_away_team=injury_reports_away_team,
                               injury_reports_home_team=injury_reports_home_team)

        mlbdb.add(game_model)
        mlbdb.commit()

        return game_model.as_dict()

    @staticmethod
    def delete_game(game_id):
        game_model = GameModel.get_game_by_id(game_id=game_id, return_as_model=True)

        if game_model:
            mlbdb.delete(game_model)
            mlbdb.commit()

            return game_model.as_dict()

        return None

