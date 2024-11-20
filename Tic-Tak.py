from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

# Constants for the game
EMPTY = " "
PLAYER = "X"
AI = "O"

# Function to check if the game is over
def check_winner(board):
    for i in range(3):
        if board[i, :].tolist() == [PLAYER] * 3 or board[:, i].tolist() == [PLAYER] * 3:
            return PLAYER
        if board[i, :].tolist() == [AI] * 3 or board[:, i].tolist() == [AI] * 3:
            return AI

    if (board.diagonal().tolist() == [PLAYER] * 3 or 
        np.fliplr(board).diagonal().tolist() == [PLAYER] * 3):
        return PLAYER
    if (board.diagonal().tolist() == [AI] * 3 or 
        np.fliplr(board).diagonal().tolist() == [AI] * 3):
        return AI

    if np.all(board != EMPTY):
        return "Tie"

    return None

# Minimax algorithm to find the best move
def minimax(board, depth, is_maximizing):
    scores = {PLAYER: -1, AI: 1, "Tie": 0}
    result = check_winner(board)

    if result is not None:
        return scores[result]

    if is_maximizing:
        best_score = -np.inf
        for i in range(3):
            for j in range(3):
                if board[i, j] == EMPTY:
                    board[i, j] = AI
                    score = minimax(board, depth + 1, False)
                    board[i, j] = EMPTY
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = np.inf
        for i in range(3):
            for j in range(3):
                if board[i, j] == EMPTY:
                    board[i, j] = PLAYER
                    score = minimax(board, depth + 1, True)
                    board[i, j] = EMPTY
                    best_score = min(score, best_score)
        return best_score

# Function for AI to choose the best move
def best_move(board):
    best_score = -np.inf
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i, j] == EMPTY:
                board[i, j] = AI
                score = minimax(board, 0, False)
                board[i, j] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

# Flask Routes
@app.route('/')
def home():
    return render_template('Tic-Tak.html')

@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    board = np.array(data['board'])
    result = check_winner(board)

    if result:
        return jsonify({"winner": result})

    # AI makes a move
    row, col = best_move(board)
    board[row, col] = AI
    result = check_winner(board)

    return jsonify({
        "board": board.tolist(),
        "winner": result,
        "move": [row, col]
    })

if __name__ == '__main__':
    app.run(debug=True)
