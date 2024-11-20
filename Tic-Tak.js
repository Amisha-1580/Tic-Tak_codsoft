const boardElement = document.getElementById("board");
const messageElement = document.getElementById("message");
const startButton = document.getElementById("startBtn");
const exitButton = document.getElementById("exitBtn");

let board = Array(3).fill(null).map(() => Array(3).fill(null));
let currentPlayer = "X";
let gameActive = false;

function createBoard() {
    boardElement.innerHTML = "";
    board.forEach((row, i) => {
        row.forEach((cell, j) => {
            const cellElement = document.createElement("div");
            cellElement.className = "cell";
            cellElement.dataset.row = i;
            cellElement.dataset.col = j;
            cellElement.addEventListener("click", handleCellClick);
            boardElement.appendChild(cellElement);
        });
    });
}

function handleCellClick(event) {
    const row = event.target.dataset.row;
    const col = event.target.dataset.col;

    if (board[row][col] || !gameActive) return;

    board[row][col] = currentPlayer;
    event.target.textContent = currentPlayer;
    const winner = checkWinner();
    if (winner) {
        messageElement.textContent = `Congratulations! ${winner} wins!`;
        gameActive = false;
        return;
    }
    

    currentPlayer = currentPlayer === "X" ? "O" : "X";
}

function checkWinner() {
    // Check rows, columns, and diagonals for a winner
    for (let i = 0; i < 3; i++) {
        if (board[i][0] && board[i][0] === board[i][1] && board[i][1] === board[i][2]) {
            return board[i][0];
        }
        if (board[0][i] && board[0][i] === board[1][i] && board[2][i] === board[1][i]) {
            return board[0][i];
        }
    }
    if (board[0][0] && board[0][0] === board[1][1] && board[1][1] === board[2][2]) {
        return board[0][0];
    }
    if (board[0][2] && board[0][2] === board[1][1] && board[1][1] === board[2][0]) {
        return board[0][2];
    }
    if (board.flat().every(cell => cell)) {
        return "Tie";
    }
    return null;
}

startButton.addEventListener("click", () => {
    board = Array(3).fill(null).map(() => Array(3).fill(null));
    currentPlayer = "X";
    gameActive = true;
    messageElement.textContent = "";
    createBoard();
});

exitButton.addEventListener("click", () => {
    window.close(); // This may not work in some browsers
});

// Initialize the game board
createBoard();