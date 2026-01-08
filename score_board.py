import numpy as np

#Tính điểm của 1 window
def evaluate_window(window, player):
    score = 0
    opponent = -player
    
    window = list(window)

    cp = window.count(player)
    co = window.count(opponent)
    ce = window.count(0)

    if cp == 5: 
        return 1000000
    if cp == 4 and ce == 1: 
        score += 10000  
    if cp == 3 and ce == 2: 
        if window == [0, player, player, player, 0]:
            score += 5000
        else:
            score += 500
    if cp == 2 and ce == 3: 
        score += 100 
    if cp == 1 and ce == 4: 
        score += 1

    if co == 5: 
        return -1000000
    if co == 4 and ce == 1: 
        score -= 80000
    if co == 3 and ce == 2: 
        if window == [0, opponent, opponent, opponent, 0]:
            score -= 40000
        else:
            score -= 2000
    if co == 2 and ce == 3: 
        score -= 200 

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
            window = np.array([board[r + i, c + i] for i in range(5)])
            total_score += evaluate_window(window, player)

    #Quét theo đường chéo phụ
    for r in range(rows - 4):
        for c in range(4, cols):
            sub_matrix = board[r : r +5, c-4: c+1]
            window = np.fliplr(sub_matrix).diagonal()
            total_score += evaluate_window(window, player)
    
    return total_score

