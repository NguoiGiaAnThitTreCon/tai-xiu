from app import app
from game_state import start_game_loop
from threading import Thread

Thread(target=start_game_loop, daemon=True).start()
