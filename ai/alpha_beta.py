from check_win_all import check_win_all
from score_board import get_total_score
from ai.heristic import get_potential_moves

def minimax_alpha_beta(board, depth, alpha, beta, maximizingPlayer):
    global node_count

    if depth == 0 or check_win_all(board):
        return get_total_score(board, -1) - get_total_score(board, 1)
    
    valid_moves = get_potential_moves(board)
    if maximizingPlayer == -1:
        maxVal = -float('inf')
        for r, c in valid_moves:
            board[r, c] = -1
            node_count += 1
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, -maximizingPlayer)
            board[r, c] = 0
            maxVal = max(maxVal, eval)
            alpha = max(alpha, eval)

            if beta <= alpha:
                break
    else:
        minVal = float('inf')
        for r, c in valid_moves:
            board[r, c] = 1
            node_count += 1
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, -maximizingPlayer)
            board[r, c] = 0
            minVal = min(minVal, eval)
            
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minVal
    
def get_alpha_beta_moves(board, depth):
    global node_count
    node_count = 0
    alpha = -float('inf')
    beta = float('inf')
    best_score = -float('inf')
    best_move = None

    valid_moves = get_potential_moves(board)
    for r, c in valid_moves:
        board[r, c] = -1
        score = minimax_alpha_beta(board, depth - 1, alpha, beta, 1)
        board[r, c] = 0
        if score > best_score:
            best_score = score
            best_move = (r, c)
        alpha = max(alpha, best_score)
    return best_move, node_count

