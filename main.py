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
bg_color = (0,233,0)
tick = 10

# Game constant number
MAXENERMY = 3
MAXSPEED = 3
MAXPLAYERBULLET = 40
PLAYERBULLETDELAY = 400
MAXENERMYBULLET = 7
ENERMYBULLETDELAY = 300

pygame.init()
screen = pygame.display.set_mode(size)
screen.fill(bg_color)

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

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/bullet.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

player = Player()
reimu = Reimu()
dock_left = Dock(bear = 'left')
dock_right = Dock(bear = 'right')
bullet = pygame.sprite.Group()

def animate():
    screen.fill(bg_color)
    player.move()
    reimu.move()
    dock_left.move()
    dock_right.move()
    screen.blit(reimu.image, reimu.rect)
    screen.blit(player.image, player.rect)
    screen.blit(dock_left.image, dock_left.rect)
    screen.blit(dock_right.image, dock_right.rect)
    pygame.display.flip()

running = True

while running:
    animate()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False