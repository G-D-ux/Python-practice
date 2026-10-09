import random, pygame, sys, os

GAME_WIDTH = 513
GAME_HEIGHT = 512
PANEL_WIDTH = 150
PANEL_HEIGHT = 180
RESULT_WINDOW_WIDTH = 350
RESULT_WINDOW_HEIGHT = 170
RESULT_WINDOW_X = (GAME_WIDTH - RESULT_WINDOW_WIDTH) // 2
RESULT_WINDOW_Y = (GAME_HEIGHT - RESULT_WINDOW_HEIGHT) // 2 + 15
BUTTON_HEIGHT = 42


def load_img(img_name, scale=None):
    image = pygame.image.load(os.path.join("img_main", img_name))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image


rock = load_img("rock.png", (GAME_WIDTH // 3, GAME_HEIGHT // 3))
paper = load_img("paper.png", (GAME_WIDTH // 3, GAME_HEIGHT // 3))
scissor = load_img("scissor.png", (GAME_WIDTH // 3, GAME_HEIGHT // 3))
icon = load_img("logo.png",(64,64))

choice_images = {
    "rock": rock,
    "paper": paper,
    "scissor": scissor,
}

choice_order = ["rock", "paper", "scissor"]
choice_rects = {
    "rock": pygame.Rect(0, GAME_HEIGHT * 2 // 3, GAME_WIDTH // 3, GAME_HEIGHT // 3),
    "paper": pygame.Rect(GAME_WIDTH // 3, GAME_HEIGHT * 2 // 3, GAME_WIDTH // 3, GAME_HEIGHT // 3),
    "scissor": pygame.Rect(GAME_WIDTH * 2 // 3, GAME_HEIGHT * 2 // 3, GAME_WIDTH // 3, GAME_HEIGHT // 3),
}

player_choice = None
computer_choice = None
result_text = ""
player_score = 0
computer_score = 0
round_over = False

play_again_rect = pygame.Rect(RESULT_WINDOW_X + 30, RESULT_WINDOW_Y + 95, 120, BUTTON_HEIGHT)
quit_rect = pygame.Rect(RESULT_WINDOW_X + 200, RESULT_WINDOW_Y + 95, 120, BUTTON_HEIGHT)


def determine_winner(player, computer):
    if player == computer:
        return "It is a draw!"
    if (
        (player == "rock" and computer == "scissor")
        or (player == "paper" and computer == "rock")
        or (player == "scissor" and computer == "paper")
    ):
        return "You win!"
    return "Computer wins!"


def play_round(choice):
    global player_choice, computer_choice, result_text, player_score, computer_score, round_over

    player_choice = choice
    computer_choice = random.choice(choice_order)
    outcome = determine_winner(player_choice, computer_choice)
    result_text = outcome
    round_over = True

    if outcome == "You win!":
        player_score += 1
    elif outcome == "Computer wins!":
        computer_score += 1


def reset_round():
    global player_choice, computer_choice, result_text, round_over
    player_choice = None
    computer_choice = None
    result_text = ""
    round_over = False


def draw_choice_box(title, choice, x, y):
    box = pygame.Rect(x, y, PANEL_WIDTH, PANEL_HEIGHT)
    pygame.draw.rect(screen, "white", box, border_radius=10)
    pygame.draw.rect(screen, "black", box, 3, border_radius=10)

    label = small_font.render(title, True, "black")
    label_rect = label.get_rect(center=(x + PANEL_WIDTH // 2, y + 18))
    screen.blit(label, label_rect)

    if choice is not None:
        image = choice_images[choice]
        image_rect = image.get_rect(center=(x + PANEL_WIDTH // 2, y + 90))
        screen.blit(image, image_rect)
        choice_name = small_font.render(choice.title(), True, "black")
        name_rect = choice_name.get_rect(center=(x + PANEL_WIDTH // 2, y + 155))
        screen.blit(choice_name, name_rect)
    else:
        placeholder = small_font.render("Waiting...", True, "black")
        placeholder_rect = placeholder.get_rect(center=(x + PANEL_WIDTH // 2, y + 90))
        screen.blit(placeholder, placeholder_rect)


def draw_score():
    score_text = mid_font.render(f"You {player_score} - {computer_score} Computer", True, "black")
    score_rect = score_text.get_rect(center=(GAME_WIDTH // 2, 250))
    screen.blit(score_text, score_rect)


def draw_choice_buttons():
    for index, name in enumerate(choice_order):
        rect = choice_rects[name]
        screen.blit(choice_images[name], rect.topleft)
        if not round_over:
            pygame.draw.rect(screen, "yellow", rect.inflate(-10, -10), 4)


def draw_result_popup():
    popup = pygame.Rect(RESULT_WINDOW_X, RESULT_WINDOW_Y, RESULT_WINDOW_WIDTH, RESULT_WINDOW_HEIGHT)
    pygame.draw.rect(screen, "white", popup, border_radius=15)
    pygame.draw.rect(screen, "black", popup, 4, border_radius=15)

    result = big_font.render(result_text, True, "black")
    result_rect = result.get_rect(center=(RESULT_WINDOW_X + RESULT_WINDOW_WIDTH // 2, RESULT_WINDOW_Y + 45))
    screen.blit(result, result_rect)

    play_again_button = create_button("Play Again", play_again_rect.x, play_again_rect.y, play_again_rect.width, play_again_rect.height, "green")
    quit_button = create_button("Quit", quit_rect.x, quit_rect.y, quit_rect.width, quit_rect.height, "red")
    return play_again_button, quit_button


def create_button(label, x, y, width, height, color):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, "black", rect, 2, border_radius=10)
    text = mid_font.render(label, True, "black")
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)
    return rect


def draw_game():
    screen.fill("light blue")
    draw_choice_box("You", player_choice, 20, 20)
    draw_choice_box("Computer", computer_choice, 343, 20)
    draw_score()
    draw_choice_buttons()

    if round_over:
        draw_result_popup()


def toggle_fullscreen():
    global display_surface, fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        display_surface = pygame.display.set_mode(
            (GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE
        )


def map_mouse_position(pos):
    display_width, display_height = display_surface.get_size()
    scale = min(display_width / GAME_WIDTH, display_height / GAME_HEIGHT)
    rendered_width = int(GAME_WIDTH * scale)
    rendered_height = int(GAME_HEIGHT * scale)
    offset_x = (display_width - rendered_width) // 2
    offset_y = (display_height - rendered_height) // 2

    if not pygame.Rect(offset_x, offset_y, rendered_width, rendered_height).collidepoint(pos):
        return None

    return (
        int((pos[0] - offset_x) / scale),
        int((pos[1] - offset_y) / scale),
    )


pygame.init()
display_surface = pygame.display.set_mode(
    (GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE
)
screen = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
fullscreen = False
pygame.display.set_caption("Rock Paper Scissors")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
small_font = pygame.font.SysFont(None, 22)
mid_font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 32)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            toggle_fullscreen()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and fullscreen:
            toggle_fullscreen()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = map_mouse_position(event.pos)
            if pos is None:
                continue

            if round_over:
                if play_again_rect.collidepoint(pos):
                    reset_round()
                elif quit_rect.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
            else:
                for name, rect in choice_rects.items():
                    if rect.inflate(-10, -10).collidepoint(pos):
                        play_round(name)
                        break

    draw_game()

    display_width, display_height = display_surface.get_size()
    scale = min(display_width / GAME_WIDTH, display_height / GAME_HEIGHT)
    rendered_size = (int(GAME_WIDTH * scale), int(GAME_HEIGHT * scale))
    rendered = pygame.transform.scale(screen, rendered_size)

    display_surface.fill("black")
    display_surface.blit(rendered, ((display_width - rendered_size[0]) // 2, (display_height - rendered_size[1]) // 2))
    
    pygame.display.flip()
    clock.tick(60)