import json

DATA_PATH = "user_data.json"

def get_user_data() -> dict | None:
    try:
        with open(DATA_PATH, "r") as f:
            data = f.read()
            data = json.loads(data)
            return data
    except:
        return None
    
def write_user_data(data: dict) -> bool:
    try:
        with open(DATA_PATH, "w") as f:
            json_data = json.dumps(data)
            f.write(json_data)
            return True
    except Exception as e:
        return False

def get_value(game: str, key: str) -> int | None:
    try:
        data = get_user_data()
        if not data:
            raise Exception
        
        return data[game][key]
    except Exception:
        return None

def write_value(game: str, key: str, new_value: str) -> bool:
    try:
        data = get_user_data()
        if not data:
            raise Exception
        
        new_data = data
        new_data[game][key] = new_value
        success = write_user_data(new_data)
        
        if not success:
            raise Exception

        return True
    except Exception as e:
        return False
    
def update_past_scores(game: str, new_score: int) -> bool:
    try:
        new_data = get_user_data()
        if not new_data:
            raise Exception
        
        new_data[game]["past_scores"].append(new_score)

        success = write_user_data(new_data)
        if not success:
            raise Exception
        
        return True
    except:
        return False