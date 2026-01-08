from score_board import get_total_score
from check_win_all import check_win_all
from ai.heristic import get_potential_moves

def minimax(board, depth, maximizingPlayer):
    global node_count 

    if depth == 0 or check_win_all(board):
        return get_total_score(board, -1) - get_total_score(board, 1)
    
    
    valid_moves = get_potential_moves(board)

    if maximizingPlayer == -1:
        maxVal = -float('inf')
        for r, c in valid_moves:
            board[r,c] = -1
            node_count += 1
            eval = minimax(board, depth - 1, -maximizingPlayer)
            board[r,c] = 0
            maxVal = max(maxVal, eval)
        return maxVal
    else:
        minVal = float('inf')
        for r, c in valid_moves:
            board[r, c] = 1
            node_count += 1
            eval = minimax(board, depth - 1, -maximizingPlayer)
            board[r, c] = 0
            minVal = min(minVal, eval)
        return minVal

def get_minimax_moves(board, depth):
    global node_count 
    node_count = 0
    best_score = -float('inf')
    best_move = None

    valid_moves = get_potential_moves(board)
    for r, c in valid_moves:
        board[r, c] = -1
        score = minimax(board, depth - 1, 1)
        board[r, c] = 0
        if score > best_score:
            best_score = score
            best_move = (r, c)
    return best_move, node_count
        

        