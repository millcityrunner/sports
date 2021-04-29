from utils.database import mlbdb
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class PlayerGameModel(mlbdb.Model):
    __tablename__ = 'player_games'
    player_game_id = mlbdb.Column(UUID(as_uuid=True), primary_key=True)
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
    player_expectation_id = mlbdb.Column(UUID(as_uuid=True),
                                         mlbdb.ForeignKey('player_expectations.player_expectation_id'), nullable=False)
    weather_report_id = mlbdb.Column(UUID(as_uuid=True),
                                     mlbdb.ForeignKey('weather_report_id.weather_report_id'), nullable=False)
    player_team_id = mlbdb.Column(UUID(as_uuid=True),
                                  mlbdb.ForeignKey('teams.team_id'), nullable=False)
    opponent_team_id = mlbdb.Column(UUID(as_uuid=True),
                                    mlbdb.ForeignKey('teams.teams_id'), nullable=False)

    def as_dict(self):
        return {
            'player_game_id': self.player_game_id,
            'date': self.date,
            'hits': self.hits,
            'doubles': self.doubles,
            'triples': self.triples,
            'homeruns': self.homeruns,
            'at_bats': self.at_bats,
            'runs': self.runs,
            'earned_runs': self.earned_runs,
            'batter_walks': self.batter_walks,
            'strikeouts': self.strikeouts,
            'hit_by_pitches': self.hit_by_pitches,
            'sacrifice_hits': self.sacrifice_hits,
            'sacrifice_flies': self.sacrifice_flies,
            'stolen_bases': self.stolen_bases,
            'errors': self.errors,
            'grounded_into_dp': self.grounded_into_dp,
            'left_on_base': self.left_on_base,
            'runners_in_scoring_position': self.runners_in_scoring_position,
            'runs_batted_in': self.runs_batted_in,
            'pitches_thrown': self.runs_batted_in,
            'strikes_thrown': self.strikes_thrown,
            'balls_thrown': self.balls_thrown,
            'wild_pitches': self.wild_pitches,
            'strikeouts_thrown': self.strikeouts_thrown,
            'innings_pitched': self.innings_pitched,
            'batting_order_position': self.batting_order_position,
            'dome': self.dome,
            'player_expectation_id': self.player_expectation_id,
            'weather_report_id': self.weather_report_id,
            'opponent_team_id': self.opponent_team_id,
            'player_team_id': self.player_team_id,
            'game_id': self.game_id
        }

    @staticmethod
    def get_all_player_games(**filters):
        return_as_model = False

        if filters.get('return_as_model', None) is not None:
            return_as_model = filters.get('return_as_model', False)
            del filters['return_as_model']

        return PlayerGameModel.query.filter_by(filters).all() if return_as_model is False else [
            player_game_model.as_dict() for player_game_model in PlayerGameModel.query.filter_by(filters).all()]

    @staticmethod
    def get_player_game_by_id(player_game_id, return_as_model=False):
        player_game_model = PlayerGameModel.query.filter_by(player_game_id=player_game_id).first()

        if return_as_model is False:
            return player_game_model.as_dict() if player_game_model else None

        else:
            return player_game_model if player_game_model else None

    @staticmethod
    def update_player_game(player_game_id, date=None, dome=None, hits=None, doubles=None, triples=None,
                           homeruns=None, at_bats=None, runs=None, earned_runs=None,
                           batter_walks=None, strikeouts=None, hit_by_pitches=None,
                           sacrifice_hits=None, sacrifice_flies=None, stolen_bases=None, errors=None,
                           left_on_base=None, runners_in_scoring_position=None, runs_batted_in=None,
                           pitches_thrown=None, strikes_thrown=None, balls_thrown=None, wild_pitches=None,
                           strikeouts_thrown=None, innings_pitched=None, batting_order_position=None,
                           player_expectation_id=None, opponent_team_id=None, player_team_id=None,
                           weather_report_id=None, game_id=None, return_as_model=False):
        player_game_model = PlayerGameModel.get_player_game_by_id(player_game_id=player_game_id, return_as_model=True)

        if player_game_model:
            if date is not None:
                player_game_model.date = date

            if dome is not None:
                player_game_model.dome = dome

            if hits is not None:
                player_game_model.hits = hits

            if doubles is not None:
                player_game_model.doubles = doubles

            if triples is not None:
                player_game_model.triples = triples

            if homeruns is not None:
                player_game_model.homeruns = homeruns

            if at_bats is not None:
                player_game_model.at_bats = at_bats

            if runs is not None:
                player_game_model.runs = runs

            if earned_runs is not None:
                player_game_model.earned_runs = earned_runs

            if batter_walks is not None:
                player_game_model.batter_walks = batter_walks

            if strikeouts is not None:
                player_game_model.strikeouts = strikeouts

            if hit_by_pitches is not None:
                player_game_model.hit_by_pitches = hit_by_pitches

            if sacrifice_hits is not None:
                player_game_model.sacrifice_hits = sacrifice_hits

            if sacrifice_flies is not None:
                player_game_model.sacrifice_flies = sacrifice_flies

            if stolen_bases is not None:
                player_game_model.stolen_bases = stolen_bases

            if errors is not None:
                player_game_model.errors = errors

            if left_on_base is not None:
                player_game_model.left_on_base = left_on_base

            if runners_in_scoring_position is not None:
                player_game_model.runners_in_scoring_position = runners_in_scoring_position

            if runs_batted_in is not None:
                player_game_model.runs_batted_in = runs_batted_in

            if pitches_thrown is not None:
                player_game_model.pitches_thrown = pitches_thrown

            if strikes_thrown is not None:
                player_game_model.strikes_thrown = strikes_thrown

            if balls_thrown is not None:
                player_game_model.balls_thrown = balls_thrown

            if wild_pitches is not None:
                player_game_model.wild_pitches = wild_pitches

            if strikeouts_thrown is not None:
                player_game_model.strikeouts_thrown = strikeouts_thrown

            if innings_pitched is not None:
                player_game_model.innings_pitched = innings_pitched

            if batting_order_position is not None:
                player_game_model.batting_order_position = batting_order_position

            if player_expectation_id is not None:
                player_game_model.player_expectation_id = player_expectation_id

            if opponent_team_id is not None:
                player_game_model.opponent_team_id = opponent_team_id

            if player_team_id is not None:
                player_game_model.player_team_id = player_team_id

            if weather_report_id is not None:
                player_game_model.weather_report_id = weather_report_id

            if game_id is not None:
                player_game_model.game_id = game_id

            player_game_model.commit()
            return player_game_model if return_as_model else player_game_model.as_dict()

        return None

    @staticmethod
    def create_player_game(date, dome, hits, doubles, triples, homeruns, at_bats, runs, earned_runs,
                           batter_walks, strikeouts, hit_by_pitches, sacrifice_hits, sacrifice_flies, stolen_bases,
                           errors, left_on_base, runners_in_scoring_position, runs_batted_in, pitches_thrown,
                           strikes_thrown, balls_thrown, wild_pitches, strikeouts_thrown, innings_pitched,
                           batting_order_position, player_expectation_id, opponent_team_id, player_team_id,
                           weather_report_id, game_id):
        player_game_models = PlayerGameModel.get_all_player_games(date=date, dome=dome, hits=hits, doubles=doubles,
                                                                  triples=triples, homeruns=homeruns, at_bats=at_bats,
                                                                  runs=runs, earned_runs=earned_runs,
                                                                  batter_walks=batter_walks,
                                                                  strikeouts=strikeouts, hit_by_pitches=hit_by_pitches,
                                                                  sacrifice_hits=sacrifice_hits,
                                                                  sacrifice_flies=sacrifice_flies,
                                                                  stolen_bases=stolen_bases, errors=errors,
                                                                  left_on_base=left_on_base,
                                                                  runners_in_scoring_position=runners_in_scoring_position,
                                                                  runs_batted_in=runs_batted_in,
                                                                  pitches_thrown=pitches_thrown, strikes_thrown=strikes_thrown,
                                                                  balls_thrown=balls_thrown, wild_pitches=wild_pitches,
                                                                  strikeouts_thrown=strikeouts_thrown, innings_pitched=innings_pitched,
                                                                  batting_order_position=batting_order_position,
                                                                  player_expectation_id=player_expectation_id,
                                                                  opponent_team_id=opponent_team_id,
                                                                  player_team_id=player_team_id,
                                                                  weather_report_id=weather_report_id,
                                                                  game_id=game_id)

        if player_game_models:
            return [player_game_model.as_dict() for player_game_model in player_game_models]

        player_game_id = str(uuid4())
        player_game_model = PlayerGameModel(player_game_id=player_game_id, date=date, dome=dome, hits=hits,
                                            doubles=doubles,
                                            triples=triples, homeruns=homeruns, at_bats=at_bats,
                                            runs=runs, earned_runs=earned_runs,
                                            batter_walks=batter_walks,
                                            strikeouts=strikeouts, hit_by_pitches=hit_by_pitches,
                                            sacrifice_hits=sacrifice_hits,
                                            sacrifice_flies=sacrifice_flies,
                                            stolen_bases=stolen_bases, errors=errors,
                                            left_on_base=left_on_base,
                                            runners_in_scoring_position=runners_in_scoring_position,
                                            runs_batted_in=runs_batted_in,
                                            pitches_thrown=pitches_thrown, strikes_thrown=strikes_thrown,
                                            balls_thrown=balls_thrown, wild_pitches=wild_pitches,
                                            strikeouts_thrown=strikeouts_thrown, innings_pitched=innings_pitched,
                                            batting_order_position=batting_order_position,
                                            player_expectation_id=player_expectation_id,
                                            opponent_team_id=opponent_team_id,
                                            player_team_id=player_team_id,
                                            weather_report_id=weather_report_id,
                                            game_id=game_id
                                            )

        mlbdb.add(player_game_model)
        mlbdb.commit()

        return player_game_model.as_dict()

    @staticmethod
    def delete_player_game(player_game_id):
        player_game_model = PlayerGameModel.get_player_game_by_id(player_game_id=player_game_id, return_as_model=True)

        if player_game_model:
            mlbdb.delete(player_game_model)
            mlbdb.commit()

            return player_game_model.as_dict()

        return None
