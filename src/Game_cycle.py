import pygame
import random

from lib.cave.main import Cave

l=80
h=60
cave = Cave()
cave.save_cave(47,l,h,1,10,smooth_pixels=False) #True для гладкой карты, False(Быстрее) для пиксельной

class character(pygame.sprite.Sprite):

    def __init__(self, surface,pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = surface

        self.rect = self.image.get_rect() # size and position
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.mask = pygame.mask.from_surface(self.image)
        
        

class map(pygame.sprite.Sprite):

    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)

        self.image = surface

        self.rect = self.image.get_rect() # size and position

        self.mask = pygame.mask.from_surface(self.image)



def check_mask_collision(ball,map,Vx,Vy,slope_tolarance = 5):
    Flag = 0    
    if pygame.sprite.collide_mask(map,ball) != None:
        Flag = 4
        if Vx>0:
            for i in range(abs(Vx)):
                Flag = 3
                ball.rect.right -= 1
                ball.rect.bottom -= slope_tolarance
                for j in range(slope_tolarance):
                    ball.rect.bottom += 1
                    if pygame.sprite.collide_mask(map,ball) == None:
                        break
                if pygame.sprite.collide_mask(map,ball) == None:
                    return Flag


        elif Vx<0:
            for i in range(abs(Vx)):
                Flag = 3
                ball.rect.left += 1
                ball.rect.bottom -= slope_tolarance
                for j in range(slope_tolarance):
                    ball.rect.bottom += 1
                    if pygame.sprite.collide_mask(map,ball) == None:
                        break
                if pygame.sprite.collide_mask(map,ball) == None:
                    return Flag


        if Vy<0:
            Flag = 1
            for i in range(abs(Vy)):
                ball.rect.top += 1
                if pygame.sprite.collide_mask(map,ball) == None:
                    return Flag
            

        elif Vy>0:
            Flag = 2
            for i in range(abs(Vy)):
                ball.rect.bottom -= 1
                if pygame.sprite.collide_mask(map,ball) == None:
                    return Flag
    return Flag

def random_spawn(ball,cave):
    ball.rect.x = round(random.random() * cave.rect.width)
    ball.rect.y = round(random.random() * cave.rect.height)
    while check_mask_collision(ball,cave,0,0,0) != 0:
        ball.rect.x = round(random.random() * cave.rect.width)
        ball.rect.y = round(random.random() * cave.rect.height)


# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (127,127,127)

# Настройки движения
Vx_acceleration = 3
Vx_deceliration = 4
Vy0 = 15

Vx = 0
Vy = 0

Vx_max = 7
g = 1

cave = pygame.image.load("src\Textures\cave.png") 
cave = map(cave)

radius = 10

# CircleX = round(random.random() * cave.rect.width)
# CircleY = round(random.random() * cave.rect.height)
player = pygame.image.load("src\Textures\Player.png") 
# ball = pygame.Surface((radius*2,radius*2))
ball = character(player,(0,0))
random_spawn(ball,cave)

# Группировка спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add(ball)
all_sprites.add(cave)

Jump_flag = True

WIDTH = cave.rect.width
HEIGHT = cave.rect.height
FPS = 30

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


UpHeld = False
DownHeld = False
RightHeld = False
LeftHeld = False
# Цикл игры
running = True
while running:

    UpHeld = False
    Vx_flag = False
    Vy_flag = False

    all_sprites.update()
    screen.fill(GRAY)
    all_sprites.draw(screen)

    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        # Проверка тыков 
        elif event.type == pygame.KEYDOWN:
            
            if event.key ==pygame.K_a:  
                LeftHeld = True
            elif event.key == pygame.K_d:
                RightHeld = True
            elif event.key == pygame.K_SPACE:
                UpHeld = True
            # elif event.key == 115:
            #     random_spawn(ball,cave)
                # DownHeld = True

        elif event.type == pygame.KEYUP:
            if event.key ==pygame.K_a:  
                LeftHeld = False
            elif event.key == pygame.K_d:
                RightHeld = False
            # elif event.key == 119:
            #     UpHeld = False
            # elif event.key == 115:
            #     DownHeld = False

    # Если кнопка зажата, то
    if LeftHeld == RightHeld:
        if Vx>0:
            Vx = max(0,Vx-Vx_deceliration)
        else:
            Vx = min(0,Vx+Vx_deceliration)
    if RightHeld == True:
        Vx = min(Vx+Vx_acceleration,Vx_max)
    elif LeftHeld == True:
        Vx = max(Vx-Vx_acceleration,-Vx_max)
    if UpHeld:
        if Jump_flag:
            Vy = -Vy0
            Jump_flag = False

    # Движение по X
    ball.rect.x += Vx
    Vx_flag = check_mask_collision(ball,cave,Vx,0)

    # Движение по Y
    ball.rect.y += Vy 
    Vy_flag = check_mask_collision(ball,cave,0,Vy)

    # Если ударисля о пол или потолок
    if Vy_flag == 1:
        Vy = 0
    elif Vy_flag == 2:
        Vy = 0
        Jump_flag = True

    # Гравитация
    Vy +=g 

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
