from flask import Flask, render_template, request, redirect, session, jsonify
import json, os
from game_state import game_state
app = Flask(__name__)
app.secret_key = 'secret'
@app.route('/')
def login(): return redirect('/home')
@app.route('/home')
def home(): return render_template('index.html')
@app.route('/get_game_state')
def get_game_state(): return jsonify({"result": game_state.get("last_result"), "time_left": game_state["time_left"]})
