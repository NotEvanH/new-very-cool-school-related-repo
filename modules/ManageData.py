import sqlite3
import os

DB_FILE = "user_data.db"
INIT_FILE = "init_db.sql"

# INTERNAL FUNCTION

def _get_connection() -> None:
    path_exists = os.path.exists(DB_FILE)
    connection = sqlite3.connect(DB_FILE)
    if not path_exists:
        try:
            with open(INIT_FILE, "r") as f:
                connection.executescript(f.read())

            connection.commit()
        except:
            connection.close()
            print("[ERROR] Something went wrong loading data.")
    
    return connection

def _get_game_id(cursor, game: str) -> int | None:
    cursor.execute("SELECT id FROM games WHERE name = ?;", (game,))
    row = cursor.fetchone()
    return row[0] if row else None

# External Functions

def get_user_data() -> dict | None:
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        data = {}

        cursor.execute("SELECT id, name FROM games;")
        games = cursor.fetchall()
        for game_id, name in games:
            data[name] = {}

            cursor.execute("SELECT most_recent_score, winstreak, highest_winstreak FROM game_stats WHERE game_id = ?;", (game_id,))

            stats = cursor.fetchone()
            if stats:
                most_recent_score, winstreak, highest_winstreak = stats
            else:
                most_recent_score, winstreak, highest_winstreak = None

            data[name]["most_recent_score"] = most_recent_score
            
            if winstreak != None:
                data[name]["winstreak"] = winstreak
            
            if highest_winstreak != None:
                data[name]["highest_winstreak"] = highest_winstreak
            
            cursor.execute("SELECT score FROM scores WHERE game_id = ?;", (game_id,))

            scores = [row[0] for row in cursor.fetchall()]
            data[name]["past_scores"] = scores
        
        connection.close()
        return data
    except:
        return None

def write_user_data(data: dict) -> bool:
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        for game, game_data in data.items():
            game_id = _get_game_id(cursor, game)

            keys = ["most_recent_score", "winstreak", "highest_winstreak"]
            values = [game_data.get(key) for key in keys]

            columns = []
            values = []
            for key, value in zip(keys, values):
                if value != None:
                    columns.append(key)
                    values.append(value)

            if columns:
                columns_string = ", ".join(columns)
                placeholders = ", ".join(["?"] * len(columns))
                cursor.execute(f"INSERT OR REPLACE INTO game_stats (game_id, {columns_string})", [game_id] + values)

            cursor.execute("DELETE FROM scores WHERE game_id = ?;", (game_id,))

            for score in game_data.get("past_scores", []):
                cursor.execute("INSERT INTO scores (game_id, score) VALUES (?, ?);",(game_id, score))

        connection.commit()
        connection.close()
        return True
    except:
        return False

def get_value(game: str, key: str) -> int | None:
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        game_id = _get_game_id(cursor, game)
        if game_id == None:
            raise Exception
        
        if key == "past_scores":
            cursor.execute("SELECT score FROM scores WHERE game_id = ?;",(game_id,))

            past_scores = [row[0] for row in cursor.fetchall()]
            connection.close()
            return past_scores
        
        cursor.execute("SELECT most_recent_score, winstreak, highest_winstreak FROM game_stats WHERE game_id = ?;", (game_id,))

        stats = cursor.fetchone()
        connection.close()

        if not stats:
            return None
        
        mapping = {
            "most_recent_score": stats[0],
            "winstreak": stats[1],
            "highest_winstreak": stats[2]
        }

        return mapping[key]
    except:
        return None
    
def write_value(game: str, key: str, new_value) -> bool:
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        game_id = _get_game_id(cursor, game)

        if game_id == None:
            raise Exception
        
        cursor.execute("SELECT most_recent_score, winstreak, highest_winstreak FROM game_stats WHERE game_id = ?;", (game_id,))

        stats = cursor.fetchone()
        if not stats:
            stats = (None, None, None)
        
        mapping = {
            "most_recent_score": stats[0],
            "winstreak": stats[1],
            "highest_winstreak": stats[2]
        }

        mapping[key] = new_value

        cursor.execute("INSERT OR REPLACE INTO game_stats (game_id, most_recent_score, winstreak, highest_winstreak) VALUES (?, ?, ?, ?);", (
            game_id,
            mapping["most_recent_score"],
            mapping["winstreak"],
            mapping["highest_winstreak"]
        ))

        connection.commit()
        connection.close()
        return True
    except:
        return False
    
def update_past_scores(game: str, new_score: int) -> bool:
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        game_id = _get_game_id(cursor, game)
        if game_id == None:
            raise Exception
        
        cursor.execute("INSERT INTO scores (game_id, score) VALUES (?, ?);", (game_id, new_score))

        connection.commit()
        connection.close()
        return True
    except:
        return False