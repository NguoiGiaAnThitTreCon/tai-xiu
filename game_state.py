import time, random
game_state = {"time_left": 30, "last_result": {}}
def start_game_loop():
    print('🌀 Vòng chơi Tài Xỉu đang khởi động...')
    while True:
        game_state['time_left'] = 30
        for i in range(30):
            game_state['time_left'] = 30 - i
            time.sleep(1)
        dice = [random.randint(1,6) for _ in range(3)]
        total = sum(dice)
        outcome = 'Tài' if total >= 11 else 'Xỉu'
        game_state['last_result'] = {"dice": dice, "total": total, "outcome": outcome}
