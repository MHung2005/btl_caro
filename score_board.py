import numpy as np

#Tính điểm của 1 window
def evaluate_window(window, player):
    score = 0
    opponent = -player

    cp = np.count_nonzero(window == player)
    co = np.count_nonzero(window == opponent)
    ce = 5 - cp - co

    if cp == 5: return 100000
    if cp == 4 and ce == 1: score += 1000
    if cp == 3 and ce == 2: score += 100
    if cp == 2 and ce == 3: score += 10
    if cp == 1 and ce == 4: score += 1

    if co == 5: return -100000
    if co == 4 and ce == 1: score -= 1000
    if co == 3 and ce == 2: score -= 100
    if co == 2 and ce == 3: score -= 10

    return score

def get_total_score(board, player):
    total_score = 0
    rows, cols = board.shape

    #Quét theo hàng
    for r in range(rows):
        for c in range(cols - 4):
            window = board[r, c : c+5]
            total_score += evaluate_window(window, player)
    
    #Quét theo cột
    for c in range(cols):
        for r in range(rows - 4):
            window = board[r : r+5, c]
            total_score += evaluate_window(window, player)

    #Quét theo đường cheo chính
    for r in range(rows - 4):
        for c in range(cols - 4):
            window = [board[r + i, c + i] for i in range(5)]
            total_score += evaluate_window(window, player)

    #Quét theo đường chéo phụ
    for r in range(rows - 4):
        for c in range(4, cols):
            sub_matrix = board[r : r +5, c-4: c+1]
            window = np.fliplr(sub_matrix).diagonal()
            total_score += evaluate_window(window, player)
    
    return total_score

    



