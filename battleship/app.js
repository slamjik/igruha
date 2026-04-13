const SIZE = 10;
const SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1];

const boardEl = document.getElementById("enemyBoard");
const statusEl = document.getElementById("status");
const restartBtn = document.getElementById("restartBtn");

let board = [];
let remainingDecks = 0;
let isGameOver = false;

function createBoard() {
  board = Array.from({ length: SIZE }, () =>
    Array.from({ length: SIZE }, () => ({ ship: false, shot: false }))
  );

  for (const shipLength of SHIPS) {
    placeShip(shipLength);
  }

  remainingDecks = SHIPS.reduce((sum, len) => sum + len, 0);
}

function placeShip(length) {
  let placed = false;

  while (!placed) {
    const horizontal = Math.random() < 0.5;
    const row = randomInt(0, horizontal ? SIZE : SIZE - length + 1);
    const col = randomInt(0, horizontal ? SIZE - length + 1 : SIZE);

    if (canPlaceShip(row, col, length, horizontal)) {
      for (let i = 0; i < length; i++) {
        const r = horizontal ? row : row + i;
        const c = horizontal ? col + i : col;
        board[r][c].ship = true;
      }
      placed = true;
    }
  }
}

function canPlaceShip(row, col, length, horizontal) {
  for (let i = -1; i <= length; i++) {
    for (let j = -1; j <= 1; j++) {
      const r = horizontal ? row + j : row + i;
      const c = horizontal ? col + i : col + j;

      if (r < 0 || c < 0 || r >= SIZE || c >= SIZE) {
        continue;
      }

      if (board[r][c].ship) {
        return false;
      }
    }
  }
  return true;
}

function renderBoard() {
  boardEl.innerHTML = "";

  for (let row = 0; row < SIZE; row++) {
    for (let col = 0; col < SIZE; col++) {
      const cell = document.createElement("button");
      cell.type = "button";
      cell.className = "cell";
      cell.dataset.row = String(row);
      cell.dataset.col = String(col);

      const data = board[row][col];
      if (data.shot) {
        cell.classList.add(data.ship ? "hit" : "miss");
      }

      if (isGameOver || data.shot) {
        cell.classList.add("disabled");
      }

      cell.addEventListener("click", onShoot);
      boardEl.appendChild(cell);
    }
  }
}

function onShoot(event) {
  if (isGameOver) {
    return;
  }

  const row = Number(event.currentTarget.dataset.row);
  const col = Number(event.currentTarget.dataset.col);
  const cell = board[row][col];

  if (cell.shot) {
    return;
  }

  cell.shot = true;

  if (cell.ship) {
    remainingDecks -= 1;
    statusEl.textContent = "Попадание!";

    if (remainingDecks === 0) {
      isGameOver = true;
      statusEl.textContent = "Победа! Все корабли потоплены.";
    }
  } else {
    statusEl.textContent = "Мимо.";
  }

  renderBoard();
}

function resetGame() {
  isGameOver = false;
  createBoard();
  statusEl.textContent = "Стреляй по полю компьютера.";
  renderBoard();
}

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}

restartBtn.addEventListener("click", resetGame);
resetGame();
