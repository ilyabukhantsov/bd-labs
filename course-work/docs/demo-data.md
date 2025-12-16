<!--Создание команды, если потребуется в апишку вставить-->

{
            "team_name": "Test Team Alpha",
            "roster_start_date": "2025-01-01",
            "players": [{"nick": "P", "age": 25}]  
}


<!-- Может потребоватся поменять ник игрока или название команды -->
<!-- Тут апдейт простой, можно вводить много данных, однако для теста и отсуствия войны с ключиками легче поменять только название, но можно много, что видно по тестам -->
{
    "team_id": 1,
    "new_team_name": "New Team Name"
}


<!-- Я надеюсь под удаление не потребуется каких-то подсказок с синтазисом так что ниже команды которые можно вставить в пгшку при необходимости -->


DROP TABLE IF EXISTS team_active_roster CASCADE;
DROP TABLE IF EXISTS match_team CASCADE;
DROP TABLE IF EXISTS match CASCADE;
DROP TABLE IF EXISTS roster_player CASCADE;
DROP TABLE IF EXISTS roster CASCADE;
DROP TABLE IF EXISTS player_prize CASCADE;
DROP TABLE IF EXISTS team_prize CASCADE;
DROP TABLE IF EXISTS player CASCADE;
DROP TABLE IF EXISTS team CASCADE;


