import random, time, json, threading

game_state = {
    "current_round": {"bets": [], "ended": False},
    "time_left": 30,
    "last_result": {}
}

def save_result(result):
    try:
        with open("results.json", "r", encoding="utf-8") as f:
            results = json.load(f)
    except:
        results = []
    results.append(result)
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def update_users(bets, outcome):
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
    except:
        users = {}

    for bet in bets:
        user = bet["user"]
        if user in users:
            if bet["choice"] == outcome:
                users[user]["money"] += bet["amount"]
            else:
                users[user]["money"] -= bet["amount"]

    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def start_game_loop():
    while True:
        game_state["time_left"] = 30
        game_state["current_round"] = {"bets": [], "ended": False}
        for i in range(30):
            game_state["time_left"] = 30 - i
            time.sleep(1)

        dice = [random.randint(1, 6) for _ in range(3)]
        total = sum(dice)
        outcome = "Tài" if total >= 11 else "Xỉu"
        game_state["last_result"] = {"total": total, "dice": dice, "outcome": outcome, "time": time.strftime("%H:%M:%S")}
        game_state["current_round"]["ended"] = True

        update_users(game_state["current_round"]["bets"], outcome)
        save_result(game_state["last_result"])
