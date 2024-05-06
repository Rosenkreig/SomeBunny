import pygame
from sys import exit

# initialize
pygame.init()

# game screen
screen = pygame.display.set_mode((480, 360))
pygame.display.set_caption('SomeBunny')
icon = pygame.image.load('bunny.png')
clock = pygame.time.Clock()

# Background
sky = pygame.image.load('sky.jpg').convert()
ground = pygame.image.load('ground.png').convert()


# Main menu
def main_menu():
    game = pygame.font.Font(None, 52).render('SomeBunny', False, 'White')
    game_rect = game.get_rect(midtop=(240, 200))

    info1 = pygame.font.Font(None, 24).render('Press Enter to start', False, 'Black')
    info1_rect = info1.get_rect(midtop=(240, 240))

    info2 = pygame.font.Font(None, 24).render('Press Space to jump', False, 'Black')
    info2_rect = info2.get_rect(midtop=(240, 264))

    score_message = pygame.font.Font(None, 36).render('Your Score: ' + str(int(final_score/100)), False, 'Black')
    score_message_rect = score_message.get_rect(midtop=(240, 248))

    # Main-Rabbit png
    main_rabbit = pygame.image.load('main-rabbit.png')
    main_rabbit= pygame.transform.scale(main_rabbit, (128, 128)).convert_alpha()
    main_rabbit_rect = main_rabbit.get_rect(midbottom=(240, 180))

    screen.blit(main_rabbit, main_rabbit_rect)
    screen.blit(game, game_rect)
    if final_score == 0:
        screen.blit(info1, info1_rect)
        screen.blit(info2, info2_rect)
    else:
        screen.blit(score_message, score_message_rect)


game_mode = False
default_score = 0
final_score = 0


# Score
def display_score():
    current_time = pygame.time.get_ticks() - default_score
    score = pygame.font.Font(None, 25).render('Score: ' + str(int(current_time/100)), False, 'Black')
    score_rect = score.get_rect(topleft=(20, 20))
    screen.blit(score, score_rect)
    return current_time


# Stone Class
class Stone(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('stone.png')
        self.image = pygame.transform.scale(self.image, (38, 26)).convert_alpha()
        self.rect = self.image.get_rect(bottomright=(480, 265))

    def update(self):
        self.rect.x -= 5
        if self.rect.right <= 0:
            self.reset()

    def reset(self):
        self.rect.x = 480


# Stone
stone = Stone()


# BG Forest Class
class Forest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('forest.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 1
        if self.rect.right <= 0:
            self.reset()

    def reset(self):
        self.rect.x = 480


# Forest
forest1 = Forest(0, 7)
forest2 = Forest(480, 7)
all_forest = pygame.sprite.Group(forest1, forest2)


# Rabbit Class
class Rabbit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('rabbit.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(80, 260))
        self.gravity = 0
        self.is_jumping = False
        self.jump_speed = 10
        self.previous_y = self.rect.y
        self.jump_area = pygame.Rect(50, 100, 64, 160)

    def jump(self):
        if self.rect.bottom >= self.jump_area.bottom:
            self.gravity = -15
            self.is_jumping = True

    def update(self):
        if self.is_jumping:
            self.gravity += 1
            self.rect.y += self.gravity
            if self.rect.bottom >= self.jump_area.bottom:
                self.rect.bottom = self.jump_area.bottom
                self.is_jumping = False


# Rabbit
rabbit = Rabbit()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_mode:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rabbit.jump()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_mode = True
                    stone.rect.left = 600
                    default_score = pygame.time.get_ticks()

    if game_mode:
        # draw elements
        screen.blit(sky, (0, 0))
        all_forest.draw(screen)
        screen.blit(ground, (0, 260))
        screen.blit(stone.image, stone.rect)
        screen.blit(rabbit.image, rabbit.rect)
        final_score = display_score()
        # update
        stone.update()
        all_forest.update()
        rabbit.update()

        if rabbit.rect.colliderect(stone.rect):
            game_mode = False
    else:
        screen.fill("Light Blue")
        main_menu()
    pygame.display.update()
    clock.tick(60)
