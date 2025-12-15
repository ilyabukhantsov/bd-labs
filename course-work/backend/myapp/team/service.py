from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from ..models import Team, Player, Roster, RosterPlayer, TeamActiveRoster, SoftDeleteModel
from django.db.models import F


def create_team_with_roster(team_name, logo_bytes, players_data, roster_start_date, roster_end_date=None):
    try:
        with transaction.atomic():
            # team
            team = Team.objects.create(name=team_name, logo=logo_bytes)

            # 2. roster
            roster = Roster(team=team, start_date=roster_start_date, end_date=roster_end_date)
            roster.clean()
            roster.save()

            # 3. player
            roster_players = []
            for pdata in players_data:
                nick = pdata.get('nick')
                age = pdata.get('age')
                player = Player.objects.create(nick=nick, age=age)
                rp = RosterPlayer.objects.create(roster=roster, player=player)
                roster_players.append(rp)

            # 4. act-roster
            active_roster = TeamActiveRoster(team=team, roster=roster, start_date=roster_start_date, end_date=roster_end_date)
            active_roster.clean()
            active_roster.save()

            return {
                "team_id": team.id,
                "roster_id": roster.id,
                "player_ids": [rp.player.id for rp in roster_players],
                "active_roster_id": active_roster.id
            }

    except ValidationError as ve:
        # valid
        return {"error": "Validation error", "details": ve.message_dict if hasattr(ve, "message_dict") else str(ve)}

    except IntegrityError as ie:
        # no fk
        return {"error": "Integrity error", "details": str(ie)}

    except Exception as e:
        # other exception
        return {"error": "Unexpected error", "details": str(e)}


def update_team_and_roster(team_id, new_team_name=None, new_logo_bytes=None, roster_updates=None):
    """
    roster_updates = {
        "roster_id": int,         
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD" (optional),
        "players": [
            {"player_id": 1, "nick": "NewNick", "age": 21},
            ...
        ]
    }
    """

    try:
        with transaction.atomic():
            team = Team.objects.select_for_update().get(id=team_id)

            # upd team
            if new_team_name:
                team.name = new_team_name
            if new_logo_bytes:
                team.logo = new_logo_bytes
            team.full_clean()
            team.save()

            if roster_updates:
                roster = Roster.objects.select_for_update().get(id=roster_updates["roster_id"], team=team)

                # upd roster
                if "start_date" in roster_updates:
                    roster.start_date = roster_updates["start_date"]
                if "end_date" in roster_updates:
                    roster.end_date = roster_updates["end_date"]
                roster.clean()
                roster.save()

                # upd player
                if "players" in roster_updates:
                    for pdata in roster_updates["players"]:
                        player = Player.objects.select_for_update().get(id=pdata["player_id"])
                        if "nick" in pdata:
                            player.nick = pdata["nick"]
                        if "age" in pdata:
                            player.age = pdata["age"]
                        player.full_clean()
                        player.save()

            return {"success": True, "team_id": team.id}

    except Team.DoesNotExist:
        return {"error": "Team not found"}

    except Roster.DoesNotExist:
        return {"error": "Roster not found"}

    except Player.DoesNotExist:
        return {"error": "Player not found"}

    except ValidationError as ve:
        return {"error": "Validation error", "details": ve.message_dict if hasattr(ve, "message_dict") else str(ve)}

    except IntegrityError as ie:
        return {"error": "Integrity error", "details": str(ie)}

    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}



def hard_delete_team(team_id):
    try:
        with transaction.atomic():
            team = Team.objects.get(id=team_id)
            team.delete()  
            return {"success": True, "team_id": team_id}
    except Team.DoesNotExist:
        return {"error": "Team not found"}
    except IntegrityError as ie:
        return {"error": "Integrity error", "details": str(ie)}
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}


def soft_delete_player(player_id):
    try:
        with transaction.atomic():
            player = Player.objects.get(id=player_id)
            player.soft_delete()
            return {"success": True, "player_id": player_id}
    except Player.DoesNotExist:
        return {"error": "Player not found"}
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}