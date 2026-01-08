import numpy as np

def check_win_all(board):
    rows, cols = board.shape
    win_condition = 5

    for i in range(rows):
        for j in range(cols):
            player = board[i,j]
            
            if player == 0:
                continue
            
            #kiểm tra hàng ngang
            if j + win_condition <= cols:
                if np.all(board[i, j: j + win_condition] == player):
                    return player
                
            #kiểm tra cột dọc
            if i + win_condition <= rows:
                if np.all(board[i: i + win_condition, j] == player):
                    return player
                
            #kiểm tra đường chéo chính
            if i + win_condition <= rows and j + win_condition <= cols:
                sub_matrix = board[i : i + win_condition, j : j + win_condition]
                if (np.all(np.diagonal(sub_matrix) == player)):
                    return player
            
            #kiểm tra đường chéo phụ
            if i + win_condition <= rows and j - win_condition + 1 >= 0:
                sub_matrix = board[i : i + win_condition, j - win_condition + 1: j+1]
                if (np.all(np.diagonal(np.fliplr(sub_matrix)) == player)):
                    return player
                
    return 0