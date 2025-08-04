const music = document.getElementById(bg-music);
const toggleMusicBtn = document.getElementById(toggle-music);
let isPlaying = false;

toggleMusicBtn.addEventListener(click, () = {
  if (isPlaying) {
    music.pause();
    toggleMusicBtn.innerHTML = 🔈 Bật nhạc;
  } else {
    music.play();
    toggleMusicBtn.innerHTML = 🔇 Tắt nhạc;
  }
  isPlaying = !isPlaying;
});

document.addEventListener(click, () = {
  if (!isPlaying) {
    music.play().then(() = {
      isPlaying = true;
      toggleMusicBtn.innerHTML = 🔇 Tắt nhạc;
    }).catch(() = {});
  }
}, { once true });

const html = document.documentElement;
const toggleDark = document.getElementById(toggle-dark);
let dark = false;
toggleDark.addEventListener(click, () = {
  dark = !dark;
  html.setAttribute(data-bs-theme, dark  dark  light);
  toggleDark.innerHTML = dark  ☀️ Chế độ sáng  🌓 Chế độ tối;
});

function fetchGameState() {
  fetch(get_game_state)
    .then(res = res.json())
    .then(data = {
      document.getElementById(countdown).textContent = data.time_left + s;
      document.getElementById(welcome-msg).textContent = `Chào, ${data.username}! (Số dư ${data.money} VNĐ)`;

       Cập nhật kết quả xúc xắc
      if (data.result && data.result.dice) {
        const diceDisplay = data.result.dice.map(n = `🎲 ${n}`).join( - );
        document.getElementById(dice-result).textContent = diceDisplay;
        document.getElementById(sum-result).textContent = `Tổng ${data.result.total}  Kết quả ${data.result.outcome}`;
      }

       Kết quả gần đây
      const history = document.getElementById(history);
      history.innerHTML = ;
      data.results.forEach(r = {
        const li = document.createElement(li);
        li.className = list-group-item d-flex justify-content-between;
        li.innerHTML = `span${r.outcome}spansmall${r.time}small`;
        history.appendChild(li);
      });

       Leaderboard
      const lb = document.getElementById(leaderboard);
      lb.innerHTML = ;
      data.leaderboard.forEach(([name, info]) = {
        const li = document.createElement(li);
        li.className = list-group-item d-flex justify-content-between;
        li.innerHTML = `span${name}spanspan${info.money} VNĐspan`;
        lb.appendChild(li);
      });
    });
}

function fetchChat() {
  fetch(get_chat)
    .then(res = res.json())
    .then(data = {
      const chatBox = document.getElementById(chat-box);
      chatBox.innerHTML = ;
      data.forEach(entry = {
        const p = document.createElement(p);
        p.innerHTML = `strong${entry.user}strong ${entry.msg}`;
        chatBox.appendChild(p);
      });
      chatBox.scrollTop = chatBox.scrollHeight;
    });
}

setInterval(() = {
  fetchGameState();
  fetchChat();
}, 1000);

window.onload = () = {
  fetchGameState();
  fetchChat();
};
