from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    prize = models.DecimalField(max_digits=12, decimal_places=2)

    def clean(self):
        if self.start_date < timezone.now().date():
            raise ValidationError("Start date must be in the future")
        if self.prize < 0:
            raise ValidationError("Prize must be non-negative")

    def __str__(self):
        return f"{self.name} ({self.start_date.year})"


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    nick = models.CharField(max_length=50, unique=True)
    age = models.PositiveIntegerField()

    def clean(self):
        if self.age < 12:
            raise ValidationError("Player must be at least 12 years old")

    def __str__(self):
        return self.nick


class Roster(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def clean(self):
        if self.end_date and self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date")

    def __str__(self):
        return f"{self.team.name} roster ({self.start_date})"


class RosterPlayer(models.Model):
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("roster", "player")

    def __str__(self):
        return f"{self.player.nick} in {self.roster}"


class TeamPrize(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
    place = models.CharField(max_length=20)
    money = models.DecimalField(max_digits=12, decimal_places=2)

    def clean(self):
        if self.money < 0:
            raise ValidationError("Prize money must be non-negative")

    def __str__(self):
        return f"{self.roster.team.name} - {self.place} place ({self.money})"


class PlayerPrize(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    place = models.CharField(max_length=20, null=True, blank=True)
    money = models.DecimalField(max_digits=12, decimal_places=2)

    def clean(self):
        if self.money < 0:
            raise ValidationError("Prize money must be non-negative")

    def __str__(self):
        return f"{self.player.nick} - {self.place} place ({self.money})"
