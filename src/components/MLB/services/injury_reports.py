from components.MLB.models.injury_reports import InjuryReportModel
from utils.exceptions import Error


def create_injury_report(players, date, team_id):
    for player in players:
        if player.team_id != team_id:
            return Error.INVALID_VALUE

    injury_report_model = InjuryReportModel.create_injury_report(team_id=team_id, players=players, date=date)

    return injury_report_model
