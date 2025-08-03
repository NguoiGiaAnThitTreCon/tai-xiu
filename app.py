from flask import Flask, render_template, request, redirect, session, jsonify
import random, json, time, os

app = Flask(__name__)
app.secret_key = "taixiu_secret_key"

DATA_FILE = "users.json"
RESULTS_FILE = "results.json"
CHAT_FILE = "chat.json"

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

@app.route("/home", methods=["GET", "POST"])
def home():
    if "username" not in session: return redirect("/")
    users = load_data(DATA_FILE, {})
    results = load_data(RESULTS_FILE, [])
    leaderboard = sorted(users.items(), key=lambda x: x[1]["money"], reverse=True)[:5]
    return render_template("index.html", username=session["username"], money=users[session["username"]]["money"],
                           results=results[-10:], leaderboard=leaderboard)

@app.route("/bet", methods=["POST"])
def bet():
    if "username" not in session: return redirect("/")
    users = load_data(DATA_FILE, {})
    user = session["username"]
    choice = request.form["choice"]

    amount_str = request.form.get("amount", "").replace(",", "").strip()
    if not amount_str.isdigit():
        return "Số tiền không hợp lệ"

    amount = int(amount_str)
    if amount <= 0 or amount > users[user]["money"]:
        return "Số tiền không hợp lệ"

    result = random.choice(["Tài", "Xỉu"])
    win = (choice == result)
    users[user]["money"] += amount if win else -amount
    save_data(DATA_FILE, users)

    results = load_data(RESULTS_FILE, [])
    results.append({"result": result, "time": time.strftime("%H:%M:%S")})
    save_data(RESULTS_FILE, results)
    return redirect("/home")

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
    app.run(debug=True)
