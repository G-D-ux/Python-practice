import os
import sys

import pygame

pygame.init()

GAME_WIDTH = 320
GAME_HEIGHT = 320
CELL_SIZE = 64
MARGIN = 64
HUMAN = "x"
COMPUTER = "o"
WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Tic Tac Toe vs Computer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
button_font = pygame.font.SysFont(None, 26)


def load_img(filename):
    image_path = os.path.join("img_main", filename)
    return pygame.image.load(image_path).convert_alpha()


x_img = load_img("x.png")
y_img = load_img("y.png")
images = {HUMAN: x_img, COMPUTER: y_img}
board = [None] * 9
winner = None
winning_line = None
ai_move_time = None
play_again_button = pygame.Rect(35, 278, 120, 32)
quit_button = pygame.Rect(165, 278, 120, 32)


def get_result(state):
    for line in WINNING_LINES:
        a, b, c = line
        if state[a] is not None and state[a] == state[b] == state[c]:
            return state[a], line
    if all(cell is not None for cell in state):
        return "draw", None
    return None, None


def minimax(state, depth, maximizing):
    result, _ = get_result(state)
    if result == COMPUTER:
        return 10 - depth
    if result == HUMAN:
        return depth - 10
    if result == "draw":
        return 0

    available = [index for index, cell in enumerate(state) if cell is None]
    if maximizing:
        best_score = -float("inf")
        for index in available:
            state[index] = COMPUTER
            best_score = max(best_score, minimax(state, depth + 1, False))
            state[index] = None
        return best_score

    best_score = float("inf")
    for index in available:
        state[index] = HUMAN
        best_score = min(best_score, minimax(state, depth + 1, True))
        state[index] = None
    return best_score


def choose_computer_move():
    best_move = None
    best_score = -float("inf")
    for index, cell in enumerate(board):
        if cell is None:
            board[index] = COMPUTER
            score = minimax(board, 0, False)
            board[index] = None
            if score > best_score:
                best_score = score
                best_move = index
    return best_move


def play_move(index, player):
    global winner, winning_line
    if board[index] is not None or winner is not None:
        return
    board[index] = player
    winner, winning_line = get_result(board)


def draw_winning_line():
    first, _, last = winning_line
    start = pygame.Vector2(
        MARGIN + (first % 3) * CELL_SIZE + CELL_SIZE // 2,
        MARGIN + (first // 3) * CELL_SIZE + CELL_SIZE // 2,
    )
    end = pygame.Vector2(
        MARGIN + (last % 3) * CELL_SIZE + CELL_SIZE // 2,
        MARGIN + (last // 3) * CELL_SIZE + CELL_SIZE // 2,
    )
    direction = (end - start).normalize()
    start -= direction * 18
    end += direction * 18
    start = round(start.x), round(start.y)
    end = round(end.x), round(end.y)

    pygame.draw.line(screen, "white", start, end, 12)
    pygame.draw.line(screen, "red", start, end, 7)


def draw():
    screen.fill("light blue")
    for index, cell in enumerate(board):
        row, col = divmod(index, 3)
        rect = pygame.Rect(
            MARGIN + col * CELL_SIZE,
            MARGIN + row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(screen, "white", rect)
        pygame.draw.rect(screen, "black", rect, 2)
        if cell is not None:
            image_rect = images[cell].get_rect(center=rect.center)
            screen.blit(images[cell], image_rect)

    if winner == "draw":
        message = "It's a draw!"
    elif winner is not None:
        message = "You win!" if winner == HUMAN else "Computer wins!"
        draw_winning_line()
    elif ai_move_time is not None:
        message = "Computer thinking..."
    else:
        message = "Your turn (X)"

    text = font.render(message, True, "black")
    screen.blit(text, (30, 25))

    if winner is not None:
        pygame.draw.rect(screen, "white", play_again_button, border_radius=5)
        pygame.draw.rect(screen, "black", play_again_button, 2, border_radius=5)
        pygame.draw.rect(screen, "white", quit_button, border_radius=5)
        pygame.draw.rect(screen, "black", quit_button, 2, border_radius=5)
        play_text = button_font.render("Play Again", True, "black")
        quit_text = button_font.render("Quit", True, "black")
        screen.blit(play_text, play_text.get_rect(center=play_again_button.center))
        screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))


def reset_game():
    global board, winner, winning_line, ai_move_time
    board = [None] * 9
    winner = None
    winning_line = None
    ai_move_time = None


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and winner is not None:
            if play_again_button.collidepoint(event.pos):
                reset_game()
            elif quit_button.collidepoint(event.pos):
                running = False
        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and winner is None
            and ai_move_time is None
        ):
            for index in range(9):
                row, col = divmod(index, 3)
                rect = pygame.Rect(
                    MARGIN + col * CELL_SIZE,
                    MARGIN + row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )
                if rect.collidepoint(event.pos) and board[index] is None:
                    play_move(index, HUMAN)
                    if winner is None:
                        ai_move_time = pygame.time.get_ticks() + 300
                    break

    if ai_move_time is not None and pygame.time.get_ticks() >= ai_move_time:
        move = choose_computer_move()
        if move is not None:
            play_move(move, COMPUTER)
        ai_move_time = None

    draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()