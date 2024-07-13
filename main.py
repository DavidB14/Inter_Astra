#------------------- Imports -------------------
import pygame
import math
import random

#------------------- Setup Functions -------------------
WIN = pygame.display.set_mode((850, 600))
pygame.display.set_caption("Inter Astra")
pygame.font.init()

#------------------- Color Variables -------------------
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (150, 150, 150)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

#------------------- Text Variables -------------------
TITLE = pygame.font.SysFont('timesnewroman', 50)
MENU = pygame.font.SysFont('timesnewroman', 30)
TEXT = pygame.font.SysFont('timesnewroman', 20)

#------------------- Setup Variables -------------------
clock = pygame.time.Clock()
FPS = 30
clicked = False
click_timer = 0
Player = 0
enemy_list = []
bullet_list = []
enemy_multiplier = 2
game_length = 100             # Measured in seconds

#------------------- Classes -------------------
class player():
    def __init__(self):
        self.width = 25
        self.height = 25
        self.box = pygame.Rect(WIN.get_width()//2 - self.width//2, WIN.get_width()//2 - self.height//2, self.width, self.height)
        self.orientation = 0
        self.shoot_timer = pygame.time.get_ticks()
        self.sprite = pygame.image.load("Player.png")

    def get_image(self):
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        image.blit(self.sprite, (0, 0))
        image = pygame.transform.rotate(image, self.orientation)
        return image

    def move_self(self):
        if pygame.key.get_pressed()[pygame.K_a]:
            self.orientation += 3
        elif pygame.key.get_pressed()[pygame.K_d]:
            self.orientation -= 3
        elif pygame.key.get_pressed()[pygame.K_SPACE] and pygame.time.get_ticks() - self.shoot_timer >= 500:
            self.shoot_timer = pygame.time.get_ticks()
            self.shoot()

    def shoot(self):
        bullet_list.append(bullet(self.orientation, len(bullet_list)))

    def draw_self(self):
        WIN.blit(self.get_image(), (WIN.get_width()//2 - self.width//2, WIN.get_height()//2 - self.height//2))

class bullet():
    def __init__(self, angle, index):
        self.width = 10
        self.height = 4
        self.orientation = angle
        self.box = pygame.Rect(WIN.get_width()//2 + (math.sin(math.radians(self.orientation)) * 10), WIN.get_height()//2 + (math.cos(math.radians(self.orientation)) * 10), self.width, self.height)
        self.index = index
        self.extra_x = 0
        self.extra_y = 0

    def get_image(self):
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        pygame.draw.rect(image, RED, pygame.Rect(0, 0, self.width, self.height))
        image = pygame.transform.rotate(image, self.orientation)
        return image

    def move_self(self):
        self.extra_x += math.sin(math.radians(self.orientation)) - int(math.sin(math.radians(self.orientation)))
        if self.extra_x >= 1:
            self.box.x += self.extra_x
            self.extra_x -= 1
        self.box.x += math.sin(math.radians(self.orientation))
        self.extra_y += math.cos(math.radians(self.orientation)) - int(math.cos(math.radians(self.orientation)))
        if self.extra_y >= 1:
            self.box.y += self.extra_y
            self.extra_y -= 1
        self.box.y += math.cos(math.radians(self.orientation))
        if self.box.x <= 0 or self.box.x >= WIN.get_width() or self.box.y <= 0 or self.box.y >= WIN.get_height():
            bullet_list.pop(self.index)
            for bullet in bullet_list[(self.index):]:
                bullet.index -= 1

    def draw_self(self):
        WIN.blit(self.get_image(), (self.box.x, self.box.y))

class enemy():
    def __init__(self, index):
        self.width = 25
        self.height = 21
        self.orientation = random.randint(-180, 180)
        self.box = pygame.Rect(WIN.get_width()//2 + math.sin(math.radians(self.orientation)) * 100 + (math.sin(math.radians(self.orientation)) - int(math.sin(math.radians(self.orientation)))) * 100, WIN.get_height()//2 + math.cos(math.radians(self.orientation)) * 100 + (math.cos(math.radians(self.orientation)) - int(math.cos(math.radians(self.orientation)))) * 100, self.width, self.height)
        self.index = index
        self.sprite = pygame.image.load("Enemy.png")
        self.move_x_timer = pygame.time.get_ticks()
        self.move_y_timer = pygame.time.get_ticks()

    def get_image(self):
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        image.blit(self.sprite, (0, 0))
        image = pygame.transform.rotate(image, self.orientation)
        return image

    def move_self(self):
        self.collide_self()
        if  pygame.time.get_ticks() - self.move_x_timer >= 200:
            if self.box.x > WIN.get_width()//2:
                self.move_x_timer = pygame.time.get_ticks()
                self.box.x -= 1
            elif self.box.x < WIN.get_width()//2:
                self.move_x_timer = pygame.time.get_ticks()
                self.box.x += 1
        if  pygame.time.get_ticks() - self.move_y_timer >= 200:
            if self.box.y > WIN.get_height()//2:
                self.move_y_timer = pygame.time.get_ticks()
                self.box.y -= 1
            elif self.box.y < WIN.get_height()//2:
                self.move_y_timer = pygame.time.get_ticks()
                self.box.y += 1

    def collide_self(self):
        global enemy_list
        global bullet_list
        for bullet in bullet_list:                      # Bullet collision
            if self.box.colliderect(bullet.box):
                enemy_list.pop(self.index)
                if self.index < len(enemy_list):
                    for enemy2 in enemy_list[(self.index):]:
                        enemy2.index -= 1
                for _ in range(0, enemy_multiplier):
                    enemy_list.append(enemy(len(enemy_list)))
                bullet_list.pop(bullet.index)
                for bullet2 in bullet_list[(bullet.index):]:
                    bullet2.index -= 1
        if self.box.x in range(WIN.get_width()//2 - 40, WIN.get_width()//2 + 13) and self.box.y in range(WIN.get_height()//2 - 35, WIN.get_height()//2 + 13):
            lose()

    def draw_self(self):
        WIN.blit(self.get_image(), (self.box.x, self.box.y))

#------------------- Startup Functions -------------------
def startup():
    menu()

#------------------- Menu Functions -------------------
def menu():
    global clicked
    global click_timer
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - click_timer >= 200:
            clicked = True
            click_timer = pygame.time.get_ticks()
        else:
            clicked = False
        menu_draw()

def menu_draw():
    WIN.fill(BLACK)
    menu_select()
    WIN.blit(TITLE.render("Inter Astra", 1, WHITE), (WIN.get_width()//2 - TITLE.render("Inter Astra", 1, WHITE).get_width()//2, 10))
    WIN.blit(MENU.render("Play", 1, WHITE), (WIN.get_width()//2 - MENU.render("Play", 1, WHITE).get_width()//2, 150))
    WIN.blit(MENU.render("Credits", 1, WHITE), (WIN.get_width()//2 - MENU.render("Credits", 1, WHITE).get_width()//2, 190))
    WIN.blit(MENU.render("Exit", 1, WHITE), (WIN.get_width()//2 - MENU.render("Exit", 1, WHITE).get_width()//2, 230))
    pygame.display.update()

def menu_select():
    x, y = pygame.mouse.get_pos()
    if x in range(WIN.get_width()//2 - MENU.render("Play", 1, WHITE).get_width()//2 - 2, WIN.get_width()//2 + MENU.render("Play", 1, WHITE).get_width()//2 + 2) and y in range(150 - 2, 150 + MENU.render("Play", 1, WHITE).get_width() + 2):
        if clicked == True:
            main()
        else:
            pygame.draw.rect(WIN, GREY, pygame.Rect(WIN.get_width()//2 - MENU.render("Play", 1, WHITE).get_width()//2 - 2, 150 - 2, MENU.render("Play", 1, WHITE).get_width() + 4, MENU.render("Play", 1, WHITE).get_height() + 4))
    elif x in range(WIN.get_width()//2 - MENU.render("Exit", 1, WHITE).get_width()//2 - 2, WIN.get_width()//2 + MENU.render("Exit", 1, WHITE).get_width()//2 + 2) and y in range(230 - 2, 230 + MENU.render("Exit", 1, WHITE).get_width() + 2):
        if clicked == True:
            quit()
        else:
            pygame.draw.rect(WIN, GREY, pygame.Rect(WIN.get_width()//2 - MENU.render("Exit", 1, WHITE).get_width()//2 - 2, 230 - 2, MENU.render("Exit", 1, WHITE).get_width() + 4, MENU.render("Exit", 1, WHITE).get_height() + 4))

#------------------- Main Game Functions -------------------
def credits():
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        credits_draw()

def credits_draw():
    WIN.fill(BLACK)
    credits_select()
    WIN.blit(TITLE.render("Credits", 1, WHITE), (WIN.get_width()//2 - TITLE.render("Credits", 1, WHITE).get_width()//2, 10))
    pygame.display.update()

def credits_select():
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        menu()

#------------------- Main Game Functions -------------------
def main():
    global Player
    global bullet_list
    global enemy_list
    Player = player()
    enemy_list = [enemy(0), enemy(1)]
    bullet_list = []
    game_timer = pygame.time.get_ticks()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        if game_length - (pygame.time.get_ticks() - game_timer)//1000 <= 0:
            win()
        Player.move_self()
        if bullet_list != []:
            for bullet in bullet_list:
                bullet.move_self()
        if enemy_list != []:
            for foe in enemy_list:
                foe.move_self()
        main_draw(game_timer)

def main_draw(game_timer):
    WIN.fill(BLACK)
    main_select()
    WIN.blit(TEXT.render("Press Esc to exit", 1, WHITE), (10, 10))
    WIN.blit(MENU.render(str(game_length - (pygame.time.get_ticks() - game_timer)//1000), 1, WHITE), (WIN.get_width()//2 - 50, 25))
    Player.draw_self()
    if enemy_list != []:
        for enemy in enemy_list:
            enemy.draw_self()
    if bullet_list != []:
        for bullet in bullet_list:
            bullet.draw_self()
    pygame.display.update()

def main_select():
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        menu()

#------------------- Win Functions -------------------
def win():
    win_timer = pygame.time.get_ticks()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        if pygame.time.get_ticks() - win_timer >= 3000:
            menu()
        draw_win()

def draw_win():
    WIN.fill(BLACK)
    WIN.blit(TITLE.render("Congratulations!", 1, WHITE), (WIN.get_width()//2 - TITLE.render("Congratulations!", 1, WHITE).get_width()//2, 10))
    WIN.blit(MENU.render("You made it to your destination.", 1, WHITE), (WIN.get_width()//2 - MENU.render("You made it to your destination.", 1, WHITE).get_width()//2, 70))
    pygame.display.update()                         # Potentially add leaderboard/points system (if time)

#------------------- Lose Functions -------------------
def lose():
    lose_timer = pygame.time.get_ticks()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        if pygame.time.get_ticks() - lose_timer >= 3000:
            menu()
        draw_lose()

def draw_lose():
    WIN.fill(BLACK)
    WIN.blit(TITLE.render("You Lose", 1, WHITE), (WIN.get_width()//2 - TITLE.render("You Lose", 1, WHITE).get_width()//2, 10))
    WIN.blit(MENU.render("Your ship was taken by pirates", 1, WHITE), (WIN.get_width()//2 - MENU.render("Your ship was taken by pirates", 1, WHITE).get_width()//2, 70))
    pygame.display.update()

#------------------- Run Game -------------------
if __name__ == '__main__':
    startup()