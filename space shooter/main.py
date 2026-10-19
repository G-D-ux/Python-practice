
from pickle import GLOBAL
from tkinter import CENTER
from tkinter.font import BOLD

import pygame, sys, os, random

# GAME VARIABLES
running = True
GAME_WIDTH = 512
GAME_HEIGHT = 512

PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20

BULLET_Y = 8 # CHANGE IF CHANGE PLAYER WIDTH

HEALTH_WIDTH = 2
HEALTH_HEIGHT = 10

PLAYER_X = GAME_WIDTH/2
PLAYER_Y = GAME_HEIGHT-PLAYER_HEIGHT*2

PLAYER_VELOCITY_X = 5
PLAYER_VELOCITY_Y = -5

ENEMY_VELOCITY_X = 5
ENEMY_VELOCITY_Y = -0.08

PLAYER_BULLET_WIDTH = 5
PLAYER_BULLET_HEIGHT = 8
PLAYER_BULLET_VELOCITY_Y = -5

FRICTION = 0.4
SCORE = 0

# CUSTOM EVENT
SHOOTING_END = pygame.USEREVENT + 0
INVINCIBLE_END = pygame.USEREVENT + 1

def load_image(img):
    image = pygame.image.load(os.path.join("img_main", img))
    return image

BG_IMG = load_image("BG.png")
PLAYER_IMG = load_image("player_img.png")
ENEMY_IMG = load_image("enemy_img.png")
PLAYER_BULLET_IMG = load_image("player_bullet.png")
HEALTH_IMG = load_image("health_img.png")
LOGO_IMG = load_image("logo.png")

pygame.init()
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("space shooter")
pygame.display.set_icon(LOGO_IMG)
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 15)
font_1 = pygame.font.SysFont(None, 24)

class Player(pygame.Rect):
    class Bullet(pygame.Rect):
        def __init__(self):
            pygame.Rect.__init__(self, player.x + BULLET_Y , player.y, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)
            self.image = PLAYER_BULLET_IMG
            self.VELOCITY_Y = PLAYER_BULLET_VELOCITY_Y
            self.used = False

    def __init__(self):
        pygame.Rect.__init__(self, PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.VELOCITY_X = 0
        self.VELOCITY_Y = 0
        self.image = PLAYER_IMG
        self.direction = 'right'
        self.shooting = False
        self.bullets = []
        self.max_health = 10
        self.health = self.max_health
        self.invinsible = False

    def set_shooting(self):
        if not self.shooting:
            self.shooting = True
            self.bullets.append(player.Bullet())
            pygame.time.set_timer(SHOOTING_END, 125, 1)

    def set_invinsible(self, milliseconds = 1000):
        self.invinsible = True
        pygame.time.set_timer(INVINCIBLE_END, milliseconds, 1) 

    def move(self):
        KEYS = pygame.key.get_pressed()
        if  KEYS[pygame.K_LEFT] or KEYS[pygame.K_a]:
            self.VELOCITY_X = -PLAYER_VELOCITY_X
            self.direction = 'left'
        if KEYS[pygame.K_RIGHT] or KEYS[pygame.K_d]:
            self.VELOCITY_X = PLAYER_VELOCITY_X
            self.direction = 'right'
        if KEYS[pygame.K_UP] or KEYS[pygame.K_w]:
            self.VELOCITY_Y = PLAYER_VELOCITY_Y
            self.direction = 'up'
        if KEYS[pygame.K_DOWN] or KEYS[pygame.K_s]:
            self.VELOCITY_Y = -PLAYER_VELOCITY_Y
            self.direction = 'down'
        if KEYS[pygame.K_SPACE]:
            player.set_shooting()

        if self.direction == 'right' and self.VELOCITY_X > 0:
            self.VELOCITY_X -= FRICTION
        elif self.direction == 'left' and self.VELOCITY_X < 0:
            self.VELOCITY_X += FRICTION
        else:
            self.VELOCITY_X = 0

        self.x += self.VELOCITY_X

        if self.x < 0:
            self.x = 0
        if self.x + PLAYER_WIDTH > GAME_WIDTH:
            self.x = GAME_WIDTH - PLAYER_WIDTH

        if self.direction == 'up' and self.VELOCITY_Y < 0:
            self.VELOCITY_Y += FRICTION
        elif self.direction == 'down' and self.VELOCITY_Y > 0:
            self.VELOCITY_Y -= FRICTION
        else:
            self.VELOCITY_Y = 0

        self.y += self.VELOCITY_Y

        if self.y < PLAYER_HEIGHT:
            self.y = PLAYER_HEIGHT
        if self.y + PLAYER_HEIGHT > GAME_HEIGHT:
            self.y = GAME_HEIGHT - PLAYER_HEIGHT

        # BULLET
        global SCORE

        for bullet in player.bullets[:]:
            bullet.y += bullet.VELOCITY_Y

            for enemy in ENEMYS[:]:
                if enemy.colliderect(bullet):
                    ENEMYS.remove(enemy)

                    if bullet in player.bullets:
                        player.bullets.remove(bullet)

                    SCORE += 500
                    break

        player.bullets = [
            bullet for bullet in player.bullets
            if bullet.y + bullet.height > 0
        ]

class Enemy(pygame.Rect):
    def __init__(self, X, Y):
        pygame.Rect.__init__(self, X, Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.y = float(Y)
        self.VELOCITY_Y = 0
        self.image = ENEMY_IMG

player = Player()
ENEMYS = []

spawn_timer = 0
next_spawn = random.randint(30, 120)

def draw(SCORE):
    screen.blit(BG_IMG, (0, 0))
    screen.blit(player.image, player)

    for enemy in ENEMYS:
        screen.blit(enemy.image, enemy)

    for bullet in player.bullets:
        screen.blit(bullet.image, bullet)

    pygame.draw.rect(screen, "light blue", (0, 0, GAME_WIDTH, 35))
    text = font_1.render(f"score : {SCORE}", True, "black")
    screen.blit(text, (GAME_WIDTH/2, 10))

    pygame.draw.rect(screen, (136, 10, 34), (0, 20,
                    HEALTH_WIDTH*player.max_health, HEALTH_HEIGHT) )
    
    for i in range(player.max_health - player.health, player.max_health):
        screen.blit(HEALTH_IMG, (i*HEALTH_WIDTH, 20,
                                 HEALTH_WIDTH, HEALTH_HEIGHT))
        
    text_1 = font.render("player health", True, "black")
    screen.blit(text_1, (0, 5))

    global running
    if player.health <= 0:
        running = False
        font_2 = pygame.font.SysFont(None, 60, BOLD)
        text_2 = font_2.render("GAME OVER", True, "white")
        screen.blit(text_2, (100, 250))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            clock.tick(60)
       
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SHOOTING_END:
            player.shooting = False
        if event.type == INVINCIBLE_END:
            player.invinsible = False

    spawn_timer += 1
    if spawn_timer >= next_spawn:
        enemy_x = random.randint(0, GAME_WIDTH - PLAYER_WIDTH)
        enemy = Enemy(enemy_x, -20)
        ENEMYS.append(enemy)
        ENEMYS = [enemy for enemy in ENEMYS if enemy.y <= GAME_HEIGHT]

        spawn_timer = 0
        next_spawn = random.randint(30, 120)


    for enemy in ENEMYS[:]:
        enemy.VELOCITY_Y += -ENEMY_VELOCITY_Y
        enemy.y += enemy.VELOCITY_Y

        if not player.invinsible and player.colliderect(enemy):
            player.health -= 1
            player.set_invinsible()

            if enemy in ENEMYS:
                ENEMYS.remove(enemy)

    ENEMYS = [
        enemy for enemy in ENEMYS
        if enemy.y <= GAME_HEIGHT
    ]


            
    player.move()
    draw(SCORE)

    pygame.display.update()
    clock.tick(60)
