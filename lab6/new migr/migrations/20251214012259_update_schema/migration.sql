-- CreateTable
CREATE TABLE "match" (
    "id" SERIAL NOT NULL,
    "tournament_id" INTEGER NOT NULL,
    "score" VARCHAR(20),

    CONSTRAINT "match_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "match_event" (
    "id" SERIAL NOT NULL,
    "match_id" INTEGER NOT NULL,
    "event_type" VARCHAR(50) NOT NULL,
    "minute" INTEGER NOT NULL,

    CONSTRAINT "match_event_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "match_team" (
    "match_id" INTEGER NOT NULL,
    "team_id" INTEGER NOT NULL,

    CONSTRAINT "match_team_pkey" PRIMARY KEY ("match_id","team_id")
);

-- CreateTable
CREATE TABLE "player" (
    "id" SERIAL NOT NULL,
    "nick" VARCHAR(50) NOT NULL,
    "age" INTEGER NOT NULL,

    CONSTRAINT "player_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "player_prize" (
    "id" SERIAL NOT NULL,
    "player_id" INTEGER NOT NULL,
    "tournament_id" INTEGER NOT NULL,
    "place" VARCHAR(20),
    "money" DECIMAL(12,2) NOT NULL,

    CONSTRAINT "player_prize_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "roster" (
    "id" SERIAL NOT NULL,
    "team_id" INTEGER NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE,

    CONSTRAINT "roster_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "roster_player" (
    "roster_id" INTEGER NOT NULL,
    "player_id" INTEGER NOT NULL,

    CONSTRAINT "roster_player_pkey" PRIMARY KEY ("roster_id","player_id")
);

-- CreateTable
CREATE TABLE "team" (
    "id" SERIAL NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "logo" BYTEA,

    CONSTRAINT "team_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "team_active_roster" (
    "team_id" INTEGER NOT NULL,
    "roster_id" INTEGER NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE,

    CONSTRAINT "team_active_roster_pkey" PRIMARY KEY ("team_id","roster_id")
);

-- CreateTable
CREATE TABLE "team_prize" (
    "id" SERIAL NOT NULL,
    "tournament_id" INTEGER NOT NULL,
    "roster_id" INTEGER NOT NULL,
    "place" VARCHAR(20) NOT NULL,
    "money" DECIMAL(12,2) NOT NULL,

    CONSTRAINT "team_prize_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "tournament" (
    "id" SERIAL NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "start_date" DATE NOT NULL,
    "prize" DECIMAL(12,2) NOT NULL,
    "year_generated" INTEGER,

    CONSTRAINT "tournament_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "player_nick_key" ON "player"("nick");

-- CreateIndex
CREATE UNIQUE INDEX "team_name_key" ON "team"("name");

-- CreateIndex
CREATE UNIQUE INDEX "tournament_name_year_generated_key" ON "tournament"("name", "year_generated");

-- AddForeignKey
ALTER TABLE "match" ADD CONSTRAINT "match_tournament_id_fkey" FOREIGN KEY ("tournament_id") REFERENCES "tournament"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "match_event" ADD CONSTRAINT "match_event_match_id_fkey" FOREIGN KEY ("match_id") REFERENCES "match"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "match_team" ADD CONSTRAINT "match_team_match_id_fkey" FOREIGN KEY ("match_id") REFERENCES "match"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "match_team" ADD CONSTRAINT "match_team_team_id_fkey" FOREIGN KEY ("team_id") REFERENCES "team"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "player_prize" ADD CONSTRAINT "player_prize_player_id_fkey" FOREIGN KEY ("player_id") REFERENCES "player"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "player_prize" ADD CONSTRAINT "player_prize_tournament_id_fkey" FOREIGN KEY ("tournament_id") REFERENCES "tournament"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "roster" ADD CONSTRAINT "roster_team_id_fkey" FOREIGN KEY ("team_id") REFERENCES "team"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "roster_player" ADD CONSTRAINT "roster_player_player_id_fkey" FOREIGN KEY ("player_id") REFERENCES "player"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "roster_player" ADD CONSTRAINT "roster_player_roster_id_fkey" FOREIGN KEY ("roster_id") REFERENCES "roster"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "team_active_roster" ADD CONSTRAINT "team_active_roster_roster_id_fkey" FOREIGN KEY ("roster_id") REFERENCES "roster"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "team_active_roster" ADD CONSTRAINT "team_active_roster_team_id_fkey" FOREIGN KEY ("team_id") REFERENCES "team"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "team_prize" ADD CONSTRAINT "team_prize_roster_id_fkey" FOREIGN KEY ("roster_id") REFERENCES "roster"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "team_prize" ADD CONSTRAINT "team_prize_tournament_id_fkey" FOREIGN KEY ("tournament_id") REFERENCES "tournament"("id") ON DELETE CASCADE ON UPDATE CASCADE;
