from pathlib import Path


HTML_CONTENT = """<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Space Invaders</title>
    <link rel="stylesheet" href="style.css" />
</head>
<body>
    <div class="wrap">
        <h1>Space Invaders</h1>
        <p class="hint">Move: Left/Right | Shoot: Space | Restart: R</p>
        <canvas id="game" width="800" height="500"></canvas>
        <p id="status"></p>
    </div>
    <script src="script.js"></script>
</body>
</html>
"""


CSS_CONTENT = """* {
    box-sizing: border-box;
}

body {
    margin: 0;
    min-height: 100vh;
    display: grid;
    place-items: center;
    background: radial-gradient(circle at top, #101933, #070b1d 70%);
    color: #d8e3ff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.wrap {
    width: min(92vw, 840px);
    text-align: center;
}

h1 {
    margin: 0 0 8px;
    letter-spacing: 2px;
}

.hint {
    margin: 0 0 12px;
    color: #93a6d9;
}

canvas {
    width: 100%;
    height: auto;
    border: 2px solid #243061;
    border-radius: 8px;
    background: #050a17;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
}

#status {
    min-height: 24px;
    margin-top: 12px;
    color: #ffd883;
    font-weight: 600;
}
"""


JS_CONTENT = """const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const statusEl = document.getElementById('status');

const W = canvas.width;
const H = canvas.height;

const state = {
    left: false,
    right: false,
    shoot: false,
    over: false,
    win: false,
    score: 0,
};

const player = {
    x: W / 2 - 24,
    y: H - 42,
    w: 48,
    h: 16,
    speed: 5,
};

const bullets = [];
const aliens = [];

const rows = 4;
const cols = 10;
const alienW = 42;
const alienH = 24;
const gap = 14;

let alienDir = 1;
let alienSpeed = 0.8;
let lastShotAt = 0;

function resetAliens() {
    aliens.length = 0;
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            aliens.push({
                x: 90 + c * (alienW + gap),
                y: 60 + r * (alienH + gap),
                w: alienW,
                h: alienH,
                alive: true,
            });
        }
    }
}

function resetGame() {
    state.left = false;
    state.right = false;
    state.shoot = false;
    state.over = false;
    state.win = false;
    state.score = 0;
    player.x = W / 2 - player.w / 2;
    bullets.length = 0;
    alienDir = 1;
    alienSpeed = 0.8;
    lastShotAt = 0;
    resetAliens();
}

function drawPlayer() {
    ctx.fillStyle = '#7af4ff';
    ctx.fillRect(player.x, player.y, player.w, player.h);
}

function drawBullets() {
    ctx.fillStyle = '#ffd66c';
    bullets.forEach((b) => ctx.fillRect(b.x, b.y, b.w, b.h));
}

function drawAliens() {
    aliens.forEach((a) => {
        if (!a.alive) return;
        ctx.fillStyle = '#8dff8b';
        ctx.fillRect(a.x, a.y, a.w, a.h);
        ctx.fillStyle = '#0f3310';
        ctx.fillRect(a.x + 8, a.y + 8, 8, 8);
        ctx.fillRect(a.x + a.w - 16, a.y + 8, 8, 8);
    });
}

function drawHud() {
    ctx.fillStyle = '#b8c8ff';
    ctx.font = '16px Segoe UI';
    ctx.fillText(`Score: ${state.score}`, 12, 24);
}

function updatePlayer() {
    if (state.left) player.x -= player.speed;
    if (state.right) player.x += player.speed;
    player.x = Math.max(0, Math.min(W - player.w, player.x));
}

function updateBullets() {
    for (let i = bullets.length - 1; i >= 0; i--) {
        bullets[i].y -= bullets[i].speed;
        if (bullets[i].y + bullets[i].h < 0) bullets.splice(i, 1);
    }
}

function updateAliens() {
    let hitEdge = false;
    let aliveCount = 0;

    for (const a of aliens) {
        if (!a.alive) continue;
        aliveCount += 1;
        a.x += alienDir * alienSpeed;
        if (a.x < 8 || a.x + a.w > W - 8) hitEdge = true;
    }

    if (hitEdge) {
        alienDir *= -1;
        for (const a of aliens) {
            if (!a.alive) continue;
            a.y += 18;
            if (a.y + a.h >= player.y) {
                state.over = true;
            }
        }
    }

    if (aliveCount === 0) {
        state.over = true;
        state.win = true;
    }
}

function intersects(a, b) {
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

function resolveCollisions() {
    for (let i = bullets.length - 1; i >= 0; i--) {
        const bullet = bullets[i];
        for (const alien of aliens) {
            if (!alien.alive) continue;
            if (intersects(bullet, alien)) {
                alien.alive = false;
                bullets.splice(i, 1);
                state.score += 10;
                break;
            }
        }
    }
}

function maybeShoot(now) {
    if (!state.shoot || now - lastShotAt < 220) return;
    bullets.push({ x: player.x + player.w / 2 - 2, y: player.y - 12, w: 4, h: 12, speed: 7 });
    lastShotAt = now;
}

function draw() {
    ctx.clearRect(0, 0, W, H);
    drawPlayer();
    drawBullets();
    drawAliens();
    drawHud();
}

function gameLoop(now) {
    if (!state.over) {
        updatePlayer();
        maybeShoot(now);
        updateBullets();
        updateAliens();
        resolveCollisions();
        draw();
        statusEl.textContent = '';
    } else {
        draw();
        statusEl.textContent = state.win
            ? `You win! Score: ${state.score}. Press R to restart.`
            : `Game over! Score: ${state.score}. Press R to restart.`;
    }

    requestAnimationFrame(gameLoop);
}

document.addEventListener('keydown', (e) => {
    if (e.code === 'ArrowLeft') state.left = true;
    if (e.code === 'ArrowRight') state.right = true;
    if (e.code === 'Space') {
        e.preventDefault();
        state.shoot = true;
    }
    if (e.code === 'KeyR' && state.over) resetGame();
});

document.addEventListener('keyup', (e) => {
    if (e.code === 'ArrowLeft') state.left = false;
    if (e.code === 'ArrowRight') state.right = false;
    if (e.code === 'Space') state.shoot = false;
});

resetGame();
requestAnimationFrame(gameLoop);
"""


def write_file(path: Path, content: str) -> None:
        path.write_text(content, encoding="utf-8")
        print(f"Created {path.name}")


def main() -> None:
        out_dir = Path.cwd()
        write_file(out_dir / "index.html", HTML_CONTENT)
        write_file(out_dir / "style.css", CSS_CONTENT)
        write_file(out_dir / "script.js", JS_CONTENT)
        print("Done. Open index.html in a browser.")


if __name__ == "__main__":
        main()
