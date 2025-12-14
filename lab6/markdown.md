Тут було декілька змін в міграціях


1. Ми прибили year_genertet, бо це сильно ламає проект
2. Змінили деякі залежності в Roster
3. Додали нову таблицю match_event


model match_event {
  id         Int    @id @default(autoincrement())
  match_id   Int
  event_type String @db.VarChar(50)
  minute     Int
  match      match  @relation(fields: [match_id], references: [id], onDelete: Cascade)
}

model tournament {
  id             Int            @id @default(autoincrement())
  name           String         @db.VarChar(100)
  start_date     DateTime       @db.Date
  prize          Decimal        @db.Decimal(12, 2)
  year_generated Int?           // заполняем вручную через Prisma
  match          match[]
  player_prize   player_prize[]
  team_prize     team_prize[]

  @@unique([name, year_generated])
}


model tournament {
  id         Int            @id @default(autoincrement())
  name       String         @db.VarChar(100)
  start_date DateTime       @db.Date
  prize      Decimal        @db.Decimal(12, 2)
  match      match[]
  player_prize player_prize[]
  team_prize team_prize[]

  @@unique([name])
}


