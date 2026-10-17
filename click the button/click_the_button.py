import pygame, sys

class Button:
    def __init__(self, text, width, height, pos, elevation):
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'

        self.text_surf = font.render(text, True, "#EEE9E9")
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = "#E84141"
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    global click
                    click += 1
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'


pygame.init()
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption('click the button')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
font1 = pygame.font.SysFont(None, 40, bold= True)

click = 0
button1 = Button('Click me', 200, 40, (150, 200), 5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("#7BBBDB")
    button1.draw()

    score = font1.render(f"score : {click}", True, "white")
    screen.blit(score, (150, 100))

    pygame.display.update()
    clock.tick(60)