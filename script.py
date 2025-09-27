import pygame, sys, random

pygame.init()

#fonts, clock, dimensions, score and screen display
small = pygame.font.Font("font.otf", 38)
big = pygame.font.Font("font.otf", 44)
clock = pygame.time.Clock()
SCREEN_HEIGHT = 900
SCREEN_WIDTH = 600
score = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#game state variables
running = True
game_active = False
game_over = False
menu_active = True

#player class with movement, jump, boundary collision checking and drawing method
class Player:
    def __init__(self): 
        self.y = (SCREEN_HEIGHT - 50) // 2
        self.x = (SCREEN_WIDTH - 60) // 2
        self.velocity = 0
        self.jump_value = -10
        self.gravity = 0.6

    def update(self):  
        self.velocity += self.gravity
        if self.velocity > 12:
            self.velocity = 12
        self.y += self.velocity
    
    def check_boundaries(self):
        if self.y + 50 <= 0 or self. y >= SCREEN_HEIGHT - 50:
            global game_active
            global menu_active
            game_active = False
            menu_active = True
            reset_game()

    def jump(self):
        self.velocity = self.jump_value
    
    def draw(self):
        self.bird = pygame.Rect(self.x, self.y, 60, 50)
        pygame.draw.rect(screen, (255, 0, 0), self.bird)

#initializing player to be used in pipe class, pipes list and last pipe time for pipe generation
player = Player()
global last_pipe_time
pipes = []
last_pipe_time = pygame.time.get_ticks()

#pipe class with update, collision checking and drawing method
class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 60
        self.gap = 240
        self.height = random.randint(100, SCREEN_HEIGHT - self.gap - 100)
        self.top = pygame.Rect(self.x, 0, self.width, self.height)
        self.bottom =  pygame.Rect(self.x, self.height + self.gap, self.width, SCREEN_HEIGHT - (self.height + self.gap)) 
        self.score_rect = pygame.Rect(self.x + self.width // 2 - 2, self.height, 4, self.gap)
        self.scored = False

    def update(self):
        self.x -= 3
        self.top.x = self.x
        self.bottom.x = self.x
        self.score_rect.x = self.x + self.width // 2 - 2
        if player.bird.colliderect(self.top) or player.bird.colliderect(self.bottom):
            global game_active
            global menu_active
            game_active = False
            menu_active = True
        if player.bird.colliderect(self.score_rect) and not self.scored:
            global score
            score += 1
            self.scored = True

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.top)
        pygame.draw.rect(screen, (0, 255, 0), self.bottom)

#basic menu with title and prompt
def menu():
    screen.fill((0, 0, 0))
    title = big.render("Flappy Bird", True, (255, 0, 0))
    prompt = small.render("ENTER to begin", True, (0, 255, 0))
    screen.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, (SCREEN_HEIGHT - title.get_height()) // 2 - 75))
    screen.blit(prompt, ((SCREEN_WIDTH - prompt.get_width()) // 2, (SCREEN_HEIGHT - prompt.get_height()) // 2))

#game function to handle drawing, updating and pipe generation/logic
def game():
    global last_pipe_time
    screen.fill((0, 0, 0))
    player.draw()
    current_time = pygame.time.get_ticks()
    if current_time - last_pipe_time > 1750:
        pipes.append(Pipe(SCREEN_WIDTH))
        last_pipe_time = current_time

    for pipe in pipes[:]:
        pipe.update()
        pipe.draw(screen)
        if pipe.x + 60 < 0:
            pipes.remove(pipe)

#resets the game and score when player dies
def reset_game():
    global pipes, score, player, last_pipe_time
    pipes = []
    score = 0
    player = Player()
    last_pipe_time = pygame.time.get_ticks()

#game loop handling events, game state and drawing
while running:
    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.KEYDOWN and menu_active:
            if event.key == pygame.K_RETURN:
                reset_game()
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
    pygame.display.set_caption(f"Score: {score}")

pygame.quit()       