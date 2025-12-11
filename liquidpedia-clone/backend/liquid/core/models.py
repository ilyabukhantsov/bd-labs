from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    prize = models.DecimalField(max_digits=12, decimal_places=2)

    # SQLite нет GENERATED AS → вычисляем вручную
    year_generated = models.IntegerField(editable=False)

    class Meta:
        unique_together = ("name", "year_generated")

    def clean(self):
        # SQLite нельзя использовать Now() в CHECK
        if self.start_date < date.today():
            raise ValidationError("Tournament must start in the future.")

        if self.prize < 0:
            raise ValidationError("Prize must be non-negative.")

    def save(self, *args, **kwargs):
        self.full_clean()
        self.year_generated = self.start_date.year
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.start_date.year})"


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    nick = models.CharField(max_length=50, unique=True)
    age = models.PositiveIntegerField()

    def clean(self):
        if self.age < 12:
            raise ValidationError("Player must be at least 12 years old.")

    def __str__(self):
        return self.nick


class Roster(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def clean(self):
        if self.end_date and self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")

    def __str__(self):
        return f"{self.team.name} roster {self.start_date}"


class RosterPlayer(models.Model):
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("roster", "player")

    def __str__(self):
        return f"{self.player.nick} in {self.roster}"


class TeamActiveRoster(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("team", "roster")


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    score = models.CharField(max_length=20, null=True, blank=True)

    def clean(self):
        if self.score:
            import re
            if not re.match(r"^[0-9]+:[0-9]+$", self.score):
                raise ValidationError("Score must match X:Y format.")

    def __str__(self):
        return f"Match {self.id}"


class MatchTeam(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("match", "team")


class TeamPrize(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
    place = models.CharField(max_length=20)
    money = models.DecimalField(max_digits=12, decimal_places=2)

    def clean(self):
        if self.money < 0:
            raise ValidationError("Prize money must be non-negative.")

    def __str__(self):
        return f"{self.roster.team.name} - {self.place} place ({self.money})"


class PlayerPrize(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    place = models.CharField(max_length=20, null=True, blank=True)
    money = models.DecimalField(max_digits=12, decimal_places=2)

    def clean(self):
        if self.money < 0:
            raise ValidationError("Prize money must be non-negative.")

    def __str__(self):
        return f"{self.player.nick} - {self.place} place ({self.money})"
