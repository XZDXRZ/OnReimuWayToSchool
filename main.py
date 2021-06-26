# FBI Warning:
# Till 2021/06/21, only God and me could understand this code.
# I guess a few months later, only God could understand it.

# 东方上学传
# 共5面
# 讲述灵梦的上学故事
# 自机：博丽灵梦
# 敌机：魔理沙——同居
#      琪露诺——妹妹（？）
#      咲夜——女仆
#      早苗——你妈
#      爱丽丝——老师

import pygame
import sys, random, time

size = (1000,650)
bg_color = (255,255,255)
tick = 10

# Game constant number
MAXPLAYERBULLET = 80
PLAYERBULLETDELAY = 20

pygame.init()
screen = pygame.display.set_mode(size)
screen.fill(bg_color)
pygame.display.set_caption("东方上学传")

player_bullets_delay = 0
player_bullets_num = 0
player_pos = []
grade = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/death_point.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (100,50)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.pos = pygame.mouse.get_pos()
        self.height = self.rect.bottom - self.rect.top
        self.width = self.rect.right - self.rect.left
        self.pos = list(self.pos)
        self.pos[0] -= self.width/2
        self.pos[1] -= self.height/2
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[0] > size[0]:
            self.pos[0] = size[0]
        if self.pos[1] < 0:
            self.pos[1] = 0
        if self.pos[1] > size[1]:
            self.pos[1] = size[1]
        self.rect.left, self.rect.top = self.pos
        return pygame.mouse.get_pos()

    def shoot(self):
        global player_bullets_num, player_bullets_delay
        if player_bullets_num <= MAXPLAYERBULLET and player_bullets_delay >= PLAYERBULLETDELAY:
            player_bullets.add(Player_Bullet(self.rect))
            player_bullets_delay = 0
            player_bullets_num += 1
        player_bullets_delay += 1

    def game_over(self):
        global GG
        if pygame.sprite.spritecollide(player, marisa_bullets, False, pygame.sprite.collide_mask):
            GG = True

class Reimu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/Reimu_up.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (100,50)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.height = self.rect.bottom - self.rect.top
        self.width = self.rect.right - self.rect.left
        self.rect.left, self.rect.top = player.rect.left - self.width/2 + player.width/2, player.rect.top - self.height/2 + player.height/2

class Marisa(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/marisa_up.png')
        self.image = pygame.transform.scale(self.image, (128, 256))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0]/2 - (self.rect.right - self.rect.left)/2, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.shoot_delay = 0
        self.blood = 100

    def shoot1(self): #第一波弹幕
        if self.shoot_delay <= 0:
            marisa_bullets.add(Marisa_Bullets())
            self.shoot_delay = 20
        for bullet in marisa_bullets.sprites():
            bullet.move1()
        self.shoot_delay -= 1

    def behit(self):
        if pygame.sprite.spritecollide(marisa, player_bullets, True, pygame.sprite.collide_mask):
            self.blood -= 1

class Marisa_Bullets(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global player_pos
        self.image = pygame.image.load('./img/gameimg/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = marisa.rect.left + (marisa.rect.right - marisa.rect.left)/2, marisa.rect.top + (marisa.rect.bottom - marisa.rect.top)/2
        self.mask = pygame.mask.from_surface(self.image)
        if player_pos != []:
            self.t = [-(self.rect.left - player_pos[0]) / 50, -(self.rect.top - player_pos[1]) / 50]
        else:
            self.t = [0, 0]

    def move1(self):
        self.rect = self.rect.move(self.t)

class Dock(pygame.sprite.Sprite):
    def __init__(self, bear):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/Dock.png')
        self.rect = self.image.get_rect()
        self.bear = bear
        if self.bear == 'left':
            self.rect.left, self.rect.top = (90, 50)
        else:
            self.rect.left, self.rect.top = (110, 50)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.height = self.rect.bottom - self.rect.top
        self.width = self.rect.right - self.rect.left
        if self.bear == 'left':
            self.rect.left, self.rect.top = player.rect.left - self.width/2 + player.width/2 - 70, player.rect.top - self.height/2 + player.height/2
        else:
            self.rect.left, self.rect.top = player.rect.left - self.width/2 + player.width/2 + 70, player.rect.top - self.height/2 + player.height/2

class Player_Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/bullet.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pos
        self.out = False

    def move(self):
        self.rect = self.rect.move([0,-5])
        if self.rect.top < 0:
            self.out = True

player = Player()
reimu = Reimu()
marisa = Marisa()
dock_left = Dock(bear = 'left')
dock_right = Dock(bear = 'right')
player_bullets = pygame.sprite.Group()
marisa_bullets = pygame.sprite.Group()

def animate():
    global player_bullets_num, player_pos
    font = pygame.font.SysFont("Times", 50)
    player.game_over()
    screen.fill(bg_color)
    player_pos = player.move()
    reimu.move()
    dock_left.move()
    dock_right.move()
    player.shoot()
    for player_bullet in player_bullets.sprites():
        player_bullet.move()
        screen.blit(player_bullet.image, player_bullet.rect)
        if player_bullet.out:
            player_bullets.remove(player_bullet)
            player_bullets_num -= 1
    screen.blit(reimu.image, reimu.rect)
    if grade == 1:
        screen.blit(marisa.image, marisa.rect)
        marisa.shoot1()
        marisa.behit()
        marisa_blood = font.render("Marisa Blood: " + str(marisa.blood), True, (0,0,0))
        screen.blit(marisa_blood, (0,0))
        for bullet in marisa_bullets.sprites():
            screen.blit(bullet.image, bullet.rect)
            if bullet.rect.left < 0 or bullet.rect.left > size[0] or bullet.rect.top > size[1]:
                bullet.kill()
    screen.blit(dock_left.image, dock_left.rect)
    screen.blit(dock_right.image, dock_right.rect)
    screen.blit(player.image, player.rect)
    pygame.display.flip()

running = True
GG = False

while running:
    animate()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.time.delay(tick)
    if GG == True:
        font = pygame.font.SysFont("Times", 70)
        gameover_text = font.render("Game Over!", True, (255, 100, 100))
        screen.fill((255,0,0))
        screen.blit(gameover_text, (340, 280))
        pygame.display.flip()
        time.sleep(1)
        break