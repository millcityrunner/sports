from utils.database import mlbdb
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class PlayerModel(mlbdb.Model):
    __tablename__ = 'players'
    player_id = mlbdb.Column(UUID(as_uuid=True), primary_key=True)
    team_id = mlbdb.Column(UUID(as_uuid=True), mlbdb.ForeignKey('teams.team_id'))
    player_name = mlbdb.Column(mlbdb.String, unique=False, nullable=False)
    bats = mlbdb.Column(mlbdb.String(1), unique=False, nullable=False)
    throws = mlbdb.Column(mlbdb.String(1), unique=False, nullable=False)
    player_position = mlbdb.Column(mlbdb.String(5), unique=False, nullable=False)
    starter = mlbdb.Column(mlbdb.Boolean, unique=False, nullable=True, default=False)

    def as_dict(self):
        return {
            'player_id': self.player_id,
            'player_name': self.player_name,
            'bats': self.bats,
            'throws': self.throws,
            'player_position': self.player_position,
            'team_id': self.team_id,
            'starter': self.starter
        }

    @staticmethod
    def get_all_players(**filters):
        return_as_model = False

        if filters.get('return_as_model', None) is not None:
            return_as_model = filters.get('return_as_model', False)
            del filters['return_as_model']

        return PlayerModel.query.filter_by(filters).all() if return_as_model is False else [player_model.as_dict() for player_model in PlayerModel.query.filter_by(filters).all()]

    @staticmethod
    def get_player_by_id(player_id, return_as_model=False):
        player_model = PlayerModel.query.filter_by(player_id=player_id).first()

        if return_as_model is False:
            return player_model.as_dict() if player_model else None

        else:
            return player_model if player_model else None

    @staticmethod
    def update_player(player_id, player_name=None, bats=None, throws=None, player_position=None, team_id=None, starter=None,
                      return_as_model=False):
        player_model = PlayerModel.get_player_by_id(player_id=player_id, return_as_model=True)

        if player_model:
            if player_name is not None:
                player_model.player_name = player_name

            if bats is not None:
                player_model.bats = bats

            if throws is not None:
                player_model.throws = throws

            if player_position is not None:
                player_model.player_position = player_position

            if team_id is not None:
                player_model.team_id = team_id

            if starter is not None:
                player_model.starter = starter

            player_model.commit()
            return player_model if return_as_model else player_model.as_dict()

        return None

    @staticmethod
    def create_player(player_name, bats, throws, player_position, starter, team_id):
        player_models = PlayerModel.get_all_players(player_name=player_name, player_positon=player_position,
                                                   team_id=team_id)

        if player_models:
            return [player_model.as_dict() for player_model in player_models]

        player_id = str(uuid4())
        player_model = PlayerModel(player_id=player_id, player_name=player_name, bats=bats,
                                   throws=throws, starter=starter, team_id=team_id)

        mlbdb.add(player_model)
        mlbdb.commit()

        return player_model.as_dict()

    @staticmethod
    def delete_player(player_id):
        player_model = PlayerModel.get_player_by_id(player_id=player_id, return_as_model=True)

        if player_model:
            mlbdb.delete(player_model)
            mlbdb.commit()

            return player_model.as_dict()

        return None

