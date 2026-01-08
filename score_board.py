import numpy as np

#Tính điểm của 1 window
def evaluate_window(window, player):
    score = 0
    opponent = -player
    
    # Chuyển window thành numpy array nếu chưa phải
    window = np.asarray(window, dtype=np.int32)

    cp = np.count_nonzero(window == player)
    co = np.count_nonzero(window == opponent)
    ce = 5 - cp - co

    # Tấn công - AI có quân
    if cp == 5: 
        return 100000
    if cp == 4 and ce == 1: 
        score += 800  # Giảm từ 1000 xuống 800
    if cp == 3 and ce == 2: 
        score += 80   # Giảm từ 100 xuống 80
    if cp == 2 and ce == 3: 
        score += 8    # Giảm từ 10 xuống 8
    if cp == 1 and ce == 4: 
        score += 1

    # Phòng thủ - Đối thủ có quân (ưu tiên cao hơn tấn công)
    if co == 5: 
        return -100000
    if co == 4 and ce == 1: 
        score -= 2000  # Tăng từ -1000 lên -2000 (phòng thủ quan trọng)
    if co == 3 and ce == 2: 
        score -= 200   # Tăng từ -100 lên -200
    if co == 2 and ce == 3: 
        score -= 20    # Tăng từ -10 lên -20

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

