import pygame
import sys
import random

pygame.init()

bg = pygame.transform.scale((pygame.image.load("background.jpg")), (600, 900))
bird = pygame.transform.scale((pygame.image.load("bird1.png")), (60, 50))
pipe = pygame.transform.scale((pygame.image.load("pipe-green.png")), (60, 400))
pipe_flipped = pygame.transform.flip(pipe, False, True)

small = pygame.font.Font("font.otf", 38)
big = pygame.font.Font("font.otf", 44)

clock = pygame.time.Clock()

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("flappy-bird")

running = True
game_active = False
game_over = False
menu_active = True

class Player:
    def __init__(self): 
        self.bird_image = bird
        self.y = (SCREEN_HEIGHT - 50) // 2
        self.x = (SCREEN_WIDTH - 60) // 2
        self.velocity = 0
        self.jump_value = -10
        self.gravity = 0.5

    def update(self):  
        self.velocity += self.gravity
        self.y += self.velocity

    def jump(self):
        self.velocity = self.jump_value
    
    def draw(self):
        screen.blit(self.bird_image, (self.x, self.y))

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - 80 - 100)

        self.top = pipe
        self.bottom = pipe_flipped

        self.top_rect = self.top.get_rect(midbottom=(self.x, self.height))
        self.bottom_rect = self.bottom.get_rect(midtop=(self.x, self.height + 80))

    def update(self):
        self.x -= 5
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        
    def draw(self, screen):
        screen.blit(self.top, self.top_rect)
        screen.blit(self.bottom, self.bottom_rect)

global last_pipe_time
pipes = []
last_pipe_time = pygame.time.get_ticks()

player = Player()

def menu():
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    title = big.render("Flappy Bird", True, (25, 0, 0))
    prompt = small.render("ENTER to begin", True, (25, 0, 0))
    screen.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, (SCREEN_HEIGHT - title.get_height()) // 2 - 75))
    screen.blit(prompt, ((SCREEN_WIDTH - prompt.get_width()) // 2, (SCREEN_HEIGHT - prompt.get_height()) // 2))

def game():
    global last_pipe_time
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    player.draw()
    current_time = pygame.time.get_ticks()
    if current_time - last_pipe_time > 1500:
        pipes.append(Pipe(SCREEN_WIDTH))
        last_pipe_time = current_time

    for pipe in pipes[:]:
        pipe.update()
        pipe.draw(screen)
        if pipe.x + 60 < 0:
            pipes.remove(pipe)


while running:
    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.KEYDOWN and menu_active:
            if event.key == pygame.K_RETURN:
                menu_active = False
                game_active = True

        if keys[pygame.K_SPACE] and game_active:
            player.jump()
    
    if menu_active:
        menu()

    if game_active:
        player.update()
        game()

    clock.tick(60)
    pygame.display.update()

pygame.quit()       