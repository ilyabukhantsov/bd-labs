# Database Schema
## SoftDeleteModel (abstract)

is_deleted — Boolean

deleted_at — DateTime

## Tournament

id — PK

name — CharField(100)

start_date — DateField

prize — Decimal(12,2)

year_generated — Integer (auto from start_date.year)

Constraints

unique_together (name, year_generated)

Relations

One Tournament → Many Matches

One Tournament → Many TeamPrizes

One Tournament → Many PlayerPrizes

## Team

id — PK

name — CharField(100), unique

logo — BinaryField

is_deleted — Boolean

deleted_at — DateTime

Relations

One Team → Many Rosters

One Team → Many MatchTeams

One Team → Many TeamActiveRosters

## Player

id — PK

nick — CharField(50), unique

age — PositiveInteger (≥12)

is_deleted — Boolean

deleted_at — DateTime

Relations

One Player → Many RosterPlayers

One Player → Many PlayerPrizes

## Roster

id — PK

team_id — FK → Team

start_date — DateField

end_date — DateField (nullable)

Validation

end_date > start_date

Relations

One Roster → Many RosterPlayers

One Roster → Many TeamActiveRosters

One Roster → Many TeamPrizes

## RosterPlayer

(Many-to-Many: Player ↔ Roster)

id — PK

roster_id — FK → Roster

player_id — FK → Player

Constraints

unique_together (roster, player)

## TeamActiveRoster

id — PK

team_id — FK → Team

roster_id — FK → Roster

start_date — DateField

end_date — DateField (nullable)

Constraints

unique_together (team, roster)

end_date > start_date

## Match

id — PK

tournament_id — FK → Tournament

score — CharField(20), format X:Y

Relations

One Match → Many MatchTeams

## MatchTeam

(Many-to-Many: Match ↔ Team)

id — PK

match_id — FK → Match

team_id — FK → Team

Constraints

unique_together (match, team)

## TeamPrize

id — PK

tournament_id — FK → Tournament

roster_id — FK → Roster

place — CharField(20)

money — Decimal(12,2)

## PlayerPrize

id — PK

player_id — FK → Player

tournament_id — FK → Tournament

place — CharField(20, nullable)

money — Decimal(12,2)



### Tournament
 ├── Match ──< MatchTeam >── Team
 ├── TeamPrize ──> Roster ──> Team
 └── PlayerPrize ──> Player

### Team
 ├── Roster ──< RosterPlayer >── Player

 └── TeamActiveRoster ──> Roster
