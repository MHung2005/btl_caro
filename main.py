import numpy as np
import pygame
from ai.heristic import get_heristic_moves
from ai.minimax import get_minimax_moves
from ai.alpha_beta import get_alpha_beta_moves

WIDTH = 600
WIDTH_SCREEN = 1100
SIZE_BOARD = 10
SQUARE_SIZE = WIDTH // SIZE_BOARD
LINE_WIDTH = 2
OFFSET = 10
HERISTIC = 0
MINIMAX = 1
ALPHA_BETA = 2

def draw_board(screen, board):
    for r in range(SIZE_BOARD):
        for c in range(SIZE_BOARD):
            pygame.draw.rect(screen, (0, 0, 0), (c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
            
            #Vẽ X
            if board[r, c] == 1:
                start_p1 = (c*SQUARE_SIZE + OFFSET, r*SQUARE_SIZE + OFFSET)
                end_p1 = ((c+1)*SQUARE_SIZE - OFFSET, (r+1)*SQUARE_SIZE - OFFSET)
                pygame.draw.line(screen, (255, 0, 0), start_p1, end_p1, LINE_WIDTH)

                start_p2 = ((c+1)*SQUARE_SIZE - OFFSET, r*SQUARE_SIZE + OFFSET)
                end_p2 = (c*SQUARE_SIZE + OFFSET, (r+1)*SQUARE_SIZE - OFFSET)
                pygame.draw.line(screen, (255, 0, 0), start_p2, end_p2, LINE_WIDTH)
            #Vẽ O
            elif board[r, c] == -1:
                center = (c*SQUARE_SIZE + SQUARE_SIZE // 2, r*SQUARE_SIZE + SQUARE_SIZE //2)
                radius = SQUARE_SIZE // 2 - OFFSET
                pygame.draw.circle(screen, (0, 0, 255), center, radius, LINE_WIDTH)

def draw_button(screen, center, text, font, is_selected):
    radius = 12

    pygame.draw.circle(screen, (0, 0, 0), center, radius, 2)
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (center[0] + 25, center[1] - 12))

    if is_selected:
        pygame.draw.circle(screen, (0, 150, 0), center, radius -4)

    return pygame.Rect(center[0] - radius, center[1] - radius, 200, radius*2)

def draw_newgame_button(screen, rect_area, text, font):
    color = (70, 130, 180)
    border_color = (0, 0, 0)

    pygame.draw.rect(screen, color, rect_area, border_radius=8)
    pygame.draw.rect(screen, border_color, rect_area, width = 2, border_radius=8)

    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect_area.center)
    screen.blit(text_surface, text_rect)

    return rect_area

def draw_logs(screen, logs, font):
    display_logs = logs[-10:]

    for i, message in enumerate(display_logs):
        log_surface = font.render(f"{message}", True, (50, 50, 50))
        screen.blit(log_surface, (620, 300 + i*25))

def check_win_optimize(board, r, c):
    rows, cols = board.shape
    player = board[r, c]

    directions = [ 
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1)
    ]

    for dr, dc in directions:
        count = 1

        for i in range(1,5):
            nr,  nc = r + i*dr, c + i*dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr, nc] == player:
                count += 1
            else:
                break
        
        for i in range(1,5):
            nr,  nc = r - i*dr, c - i*dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr, nc] == player:
                count += 1
            else:
                break

        if count >= 5:
            return player
    
    return 0

def get_ai_move_by_mode(board, mode, logs):
    if mode == HERISTIC:
        move, nodes = get_heristic_moves(board, -1)
        logs.append(f"Số node duyệt của Heristic: {nodes}")
        return move
    
    if mode == MINIMAX:
        move, nodes = get_minimax_moves(board, 2)
        logs.append(f"Số node duyệt của Minimax: {nodes}")
        return move

    if mode == ALPHA_BETA:
        move, nodes = get_alpha_beta_moves(board, 2)
        logs.append(f"Số node duyệt của alpha-beta: {nodes}")
        return move
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH_SCREEN, WIDTH))
    board = np.zeros((SIZE_BOARD, SIZE_BOARD))
    current_player = 1 #1 là người -1 là máy
    current_mode = ALPHA_BETA
    logs = ["Thông số:"]

    pos_heristic = (630, 100)
    pos_minimax = (630, 150)
    pos_alpha_beta = (630, 200)
    pos_newgame = pygame.Rect(650, 540, 100, 45)

    font = pygame.font.SysFont("tahoma", 20)
    game_over = False

    running = True
    while running:
        screen.fill((255, 255, 255))
        draw_board(screen, board)

        title_text = font.render("CHỌN CHẾ ĐỘ AI:", True, (0, 0, 0))
        screen.blit(title_text, (620, 60))

        rect_h = draw_button(screen, pos_heristic, "Heristic", font, current_mode == HERISTIC)
        rect_m = draw_button(screen, pos_minimax, "Minimax", font, current_mode == MINIMAX)
        rect_a = draw_button(screen, pos_alpha_beta, "Alpha-Beta", font, current_mode == ALPHA_BETA)
        rect_n = draw_newgame_button(screen, pos_newgame, "New Game", font)

        draw_logs(screen, logs, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_n.collidepoint(event.pos):
                    board = np.zeros((SIZE_BOARD, SIZE_BOARD))
                    current_player = 1
                    game_over = False
                    logs = ["Thông số:"]
                elif rect_h.collidepoint(event.pos):
                    current_mode = HERISTIC
                elif rect_m.collidepoint(event.pos):
                    current_mode = MINIMAX
                elif rect_a.collidepoint(event.pos):
                    current_mode = ALPHA_BETA

                elif current_player == 1 and not game_over:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]

                    col = mouseX // SQUARE_SIZE
                    row = mouseY // SQUARE_SIZE

                    if 0 <= row < SIZE_BOARD and 0 <= col < SIZE_BOARD and (board[row, col] == 0):
                        board[row, col] = 1

                        if check_win_optimize(board, row, col):
                            logs.append("Bạn đã thắng")
                            game_over = True
                        
                        current_player *= -1
        if current_player == -1 and not game_over:
            move = get_ai_move_by_mode(board, current_mode, logs)
            if move:
                row_ai , col_ai = move
                board[row_ai, col_ai] = -1

                if check_win_optimize(board, row_ai, col_ai):
                    logs.append("Máy đã thắng")
                    game_over = True
                
                current_player *= -1            
    
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()
