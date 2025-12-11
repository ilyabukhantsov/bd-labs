from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    prize = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    year_generated = models.IntegerField(editable=False)

    class Meta:
        unique_together = ('name', 'year_generated')

    def save(self, *args, **kwargs):
        self.year_generated = self.start_date.year
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.year_generated})"


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    nick = models.CharField(max_length=50, unique=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(12)])

    def __str__(self):
        return self.nick


class Roster(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='rosters')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def clean(self):
        if self.end_date and self.end_date <= self.start_date:
            raise ValidationError("end_date must be greater than start_date")

    def __str__(self):
        return f"{self.team.name} roster {self.start_date} - {self.end_date or 'present'}"


class RosterPlayer(models.Model):
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('roster', 'player')

    def __str__(self):
        return f"{self.player.nick} in {self.roster}"


class TeamActiveRoster(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def clean(self):
        if self.end_date and self.end_date <= self.start_date:
            raise ValidationError("end_date must be greater than start_date")

    class Meta:
        unique_together = ('team', 'roster')

    def __str__(self):
        return f"{self.team.name} active roster {self.start_date} - {self.end_date or 'present'}"


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    score = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^[0-9]+:[0-9]+$', message="Score must be like '1:0'")]
    )

    def __str__(self):
        return f"Match {self.id} in {self.tournament}"


class MatchTeam(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('match', 'team')

    def __str__(self):
        return f"{self.team.name} in match {self.match.id}"


class TeamPrize(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
    place = models.CharField(max_length=20)
    money = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.roster.team.name} prize {self.place} in {self.tournament}"


class PlayerPrize(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    place = models.CharField(max_length=20, blank=True, null=True)
    money = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.player.nick} prize {self.place} in {self.tournament}"
