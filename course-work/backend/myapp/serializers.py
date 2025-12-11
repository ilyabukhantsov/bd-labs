from rest_framework import serializers
from .models import (
    Tournament, Team, Player, Roster, RosterPlayer,
    TeamActiveRoster, Match, MatchTeam, TeamPrize, PlayerPrize
)

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class RosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roster
        fields = '__all__'


class RosterPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RosterPlayer
        fields = '__all__'


class TeamActiveRosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamActiveRoster
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class MatchTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchTeam
        fields = '__all__'


class TeamPrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamPrize
        fields = '__all__'


class PlayerPrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerPrize
        fields = '__all__'
