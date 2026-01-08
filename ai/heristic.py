from score_board import  get_total_score

#Chọn các nước đi tiềm năng
def get_potential_moves(board):
    moves = set()
    rows, cols = board.shape

    for i in range(rows):
        for j in range(cols):
            if (board[i, j] != 0):
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        nr, nc = i + dr, j + dc
                        if 0 <= nr < rows and 0 <= nc < cols and board[nr, nc] == 0:
                            moves.add((nr, nc))
    
    return list(moves)

# Chọn ra nước đi tốt nhất ở các nước đi tiềm năng
def get_heristic_moves(board, ai_player):
    best_score = -10**18
    best_moves = None
    opponent = -ai_player
    potential_moves = get_potential_moves(board)
    

    for r, c in potential_moves:
        board[r, c] = ai_player
        attack_score = get_total_score(board, ai_player)

        board[r,c] = opponent
        defense_score = get_total_score(board, opponent)

        board[r,c] = 0

        total_at_this_spot = attack_score - defense_score
        if total_at_this_spot > best_score:
            best_score = total_at_this_spot
            best_moves = (r, c)
            
        print(f"{r}, {c}: {best_score}")
    
    return best_moves



