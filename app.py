from flask import Flask, render_template, request, redirect, session, jsonify, url_for
import json, os
from game_state import game_state
from threading import Lock

app = Flask(__name__)
app.secret_key = "taixiu_secret_key"

DATA_FILE = "users.json"
RESULTS_FILE = "results.json"
CHAT_FILE = "chat.json"
lock = Lock()

def load_data(file, default):
    if not os.path.exists(file): return default
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = load_data(DATA_FILE, {})
        user = request.form["username"]
        pwd = request.form["password"]
        if user in users and users[user]["password"] == pwd:
            session["username"] = user
            return redirect("/home")
        return "Sai tài khoản hoặc mật khẩu"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users = load_data(DATA_FILE, {})
        user = request.form["username"]
        pwd = request.form["password"]
        if user in users:
            return "Tài khoản đã tồn tại"
        users[user] = {"password": pwd, "money": 100000}
        save_data(DATA_FILE, users)
        return redirect("/")
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/home")
def home():
    if "username" not in session:
        return redirect("/")
    return render_template("index.html", username=session["username"])

@app.route("/bet", methods=["POST"])
def bet():
    if "username" not in session:
        return redirect("/")
    user = session["username"]
    choice = request.form["choice"]
    amount = int(request.form["amount"].replace(",", ""))

    with lock:
        users = load_data(DATA_FILE, {})
        if user not in users or users[user]["money"] < amount or amount <= 0:
            return "Số tiền không hợp lệ"
        if game_state["current_round"]["ended"]:
            return "Phiên đã kết thúc, vui lòng chờ phiên tiếp theo"
        game_state["current_round"]["bets"].append({"user": user, "choice": choice, "amount": amount})
        return redirect("/home")

@app.route("/get_game_state")
def get_game_state():
    with lock:
        return jsonify({
            "time_left": game_state["time_left"],
            "result": game_state.get("last_result", {}),
            "username": session.get("username"),
            "money": load_data(DATA_FILE, {}).get(session.get("username"), {}).get("money", 0),
            "leaderboard": sorted(load_data(DATA_FILE, {}).items(), key=lambda x: x[1]["money"], reverse=True)[:5],
            "results": load_data(RESULTS_FILE, [])[-10:]
        })

@app.route("/chat", methods=["POST"])
def chat():
    if "username" not in session: return redirect("/")
    chat_log = load_data(CHAT_FILE, [])
    msg = request.form["message"]
    chat_log.append({"user": session["username"], "msg": msg})
    save_data(CHAT_FILE, chat_log)
    return redirect("/home")

@app.route("/get_chat")
def get_chat():
    chat_log = load_data(CHAT_FILE, [])
    return jsonify(chat_log[-10:])

if __name__ == "__main__":
    from threading import Thread
    from game_state import start_game_loop
    Thread(target=start_game_loop, daemon=True).start()
    app.run(debug=True)
