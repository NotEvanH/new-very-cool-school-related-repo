CREATE TABLE games (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE NOT NULL
);

CREATE TABLE game_stats (
	game_id INTEGER PRIMARY KEY,
	most_recent_score TEXT,
	winstreak INTEGER,
	highest_winstreak INTEGER,
	FOREIGN KEY (game_id) REFERENCES games(id)
);

CREATE TABLE scores (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	game_id INTEGER,
	score INTEGER,
	FOREIGN KEY (game_id) REFERENCES games(id)
);

INSERT INTO games (name) VALUES ("spelling_bee");
INSERT INTO games (name) VALUES ("wordle");

INSERT INTO game_stats (game_id, most_recent_score) VALUES (
	(SELECT id FROM games WHERE name = "spelling_bee"),
	"N/A"
);

INSERT INTO game_stats (game_id, most_recent_score, winstreak, highest_winstreak) VALUES (
	(SELECT id FROM games WHERE name = "wordle"),
	"N/A",
	0,
	0
);