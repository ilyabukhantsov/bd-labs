from django.db import connection
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from ..models import Team, Player, Roster, RosterPlayer, TeamActiveRoster, SoftDeleteModel
from django.db.models import F


def get_players_above_18():
    sql = """
        SELECT
            p.id,
            p.nick AS player_nick,
            p.age AS player_age,
            t.id AS team_id,
            t.name AS team_name
        FROM myapp_player p
        JOIN myapp_rosterplayer rp ON rp.player_id = p.id
        JOIN myapp_roster r ON r.id = rp.roster_id
        JOIN myapp_team t ON t.id = r.team_id
        WHERE p.age > 18
        ORDER BY p.age ASC
    """

    players = Player.objects.raw(sql)

    return [
        {
            "id": p.id,
            "nick": p.player_nick,
            "age": p.player_age,
            "team_id": p.team_id,
            "team_name": p.team_name,
        }
        for p in players
    ]


def get_players_alphabetical():
    sql = """
        SELECT
            p.id,
            p.nick AS nick,
            p.age AS age,
            t.id AS team_id,
            t.name AS team_name
        FROM myapp_player p
        JOIN myapp_rosterplayer rp ON rp.player_id = p.id
        JOIN myapp_roster r ON r.id = rp.roster_id
        JOIN myapp_team t ON t.id = r.team_id
        ORDER BY p.nick ASC
    """

    players = Player.objects.raw(sql)

    return [
        {
            "id": p.id,
            "nick": p.nick,
            "age": p.age,
            "team_id": p.team_id,
            "team_name": p.team_name,
        }
        for p in players
    ]


def get_team_players_analytics():
    sql = """
        WITH roster_player_count AS (
            SELECT
                r.id AS roster_id,
                t.id AS team_id,
                t.name AS team_name,
                COUNT(rp.player_id) AS players_in_roster
            FROM myapp_roster r
            JOIN myapp_team t ON t.id = r.team_id
            JOIN myapp_rosterplayer rp ON rp.roster_id = r.id
            GROUP BY r.id, t.id, t.name
        )
        SELECT
            team_id,
            team_name,
            AVG(players_in_roster) AS avg_players_per_roster,
            MAX(players_in_roster) AS max_players_in_roster,
            MIN(players_in_roster) AS min_players_in_roster
        FROM roster_player_count
        GROUP BY team_id, team_name
        HAVING AVG(players_in_roster) > 0
        ORDER BY avg_players_per_roster DESC;
    """

    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()

    return [
        {
            "team_id": row[0],
            "team_name": row[1],
            "avg_players_per_roster": float(row[2]),
            "max_players_in_roster": row[3],
            "min_players_in_roster": row[4],
        }
        for row in rows
    ]