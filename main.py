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

import pygame, sys, random

size = (1000,650)
bg_color = (255,255,255)
tick = 4

# Game constant number
MAXPLAYERBULLET = 80
PLAYERBULLETDELAY = 20

pygame.init()
screen = pygame.display.set_mode(size)
screen.fill(bg_color)

player_bullets_delay = 0
player_bullets_num = 0

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

    def shoot(self):
        global player_bullets_num, player_bullets_delay
        print(player_bullets_delay, player_bullets_num)
        if player_bullets_num <= MAXPLAYERBULLET and player_bullets_delay >= PLAYERBULLETDELAY:
            player_bullets.add(Player_Bullet(self.rect))
            player_bullets_delay = 0
            player_bullets_num += 1
        player_bullets_delay += 1

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
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

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
dock_left = Dock(bear = 'left')
dock_right = Dock(bear = 'right')
player_bullets = pygame.sprite.Group()

def animate():
    global player_bullets_num
    screen.fill(bg_color)
    player.move()
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
    screen.blit(dock_left.image, dock_left.rect)
    screen.blit(dock_right.image, dock_right.rect)
    screen.blit(player.image, player.rect)
    pygame.display.flip()

running = True

while running:
    animate()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.time.delay(tick)