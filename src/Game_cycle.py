import pygame
import random

from lib.cave.main import Cave
from lib.objects.charecter import character
from lib.objects.weapons import mele
from lib.objects.map import map
from lib.objects.map import random_spawn
from lib.animation.spritesheet_to_sprites import sheet2frames
from lib.colisions.colisions import check_mask_collision
from lib.colisions.colisions import check_ground





l=80
h=60
cave = Cave()
cave.save_cave(47,l,h,1,10,smooth_pixels=False)  # True для гладкой карты, False(Быстрее) для пиксельной

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
# Высота прыжка
Vy0 = 15

Vx = 0
Vy = 0
# Максимальная скорость по X
Vx_max = 7
# Ускорение свободного падения
g = 1

cave = map("src\Textures\cave.png")


ball = character((0,0))
random_spawn(ball,cave)
weapon = mele((ball.rect.x,ball.rect.y))
# Группировка спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add(ball)
all_sprites.add(cave)

mele_sprites = pygame.sprite.Group()
mele_sprites.add(weapon)

Jump_flag = True

WIDTH = cave.rect.width
HEIGHT = cave.rect.height
FPS = 30

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cave Game")
clock = pygame.time.Clock()


UpHeld = False
DownHeld = False
RightHeld = False
LeftHeld = False
MiningRight = False
MiningLeft = False 
onground = False
# Цикл игры
running = True
while running:
    MiningRight = False
    MiningLeft = False 
    UpHeld = False
    Vx_flag = False
    Vy_flag = False

    all_sprites.update()
    screen.fill(GRAY)

    # Отрисовка
    screen.blit(ball.image, (ball.rect.x-ball.animate.x_offset, ball.rect.y-ball.animate.y_offset))
    screen.blit(cave.image, cave.rect.topleft)
    # all_sprites.draw(screen)

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
            elif event.key == pygame.K_w:
                MiningRight = True
            elif event.key == pygame.K_s:
                MiningLeft = True

        elif event.type == pygame.KEYUP:
            if event.key ==pygame.K_a:  
                LeftHeld = False
            elif event.key == pygame.K_d:
                RightHeld = False

    # проверка стоит ли на земле
    onground_prev = onground
    onground = check_ground(ball,cave)
    # Если кнопка зажата, то 
    # Триггеры анимации движения
    if LeftHeld == RightHeld:
        if onground:
            ball.animate.Standing(ball.animate)
        if Vx>0:
            Vx = max(0,Vx-Vx_deceliration)
        else:
            Vx = min(0,Vx+Vx_deceliration)
    else:
        if onground:
            if Vx>0:
                ball.animate.Walking_right(ball.animate)
            if Vx<0:
                ball.animate.Walking_left(ball.animate)

    if not onground:
        if Vy<0:
            ball.animate.Jumping(ball.animate)
        elif Vy>0:
            ball.animate.Falling(ball.animate)

    if onground == True and onground_prev == False:
        ball.animate.Landed(ball.animate)


    if RightHeld and not LeftHeld:
        Vx = min(Vx+Vx_acceleration,Vx_max)
    elif LeftHeld and not RightHeld:
        Vx = max(Vx-Vx_acceleration,-Vx_max)
    if UpHeld:
        if Jump_flag:
            Vy = -Vy0
            Jump_flag = False

    if MiningRight:
        weapon.animate.Mining_hit_right(weapon.animate)
        
    if MiningLeft:
        weapon.animate.Mining_hit_left(weapon.animate)
    
    mele_sprites.update(ball)


    if weapon.animate.mining_hit_right or weapon.animate.mining_hit_left:
       screen.blit(weapon.image,(weapon.rect.x-weapon.animate.x_offset,weapon.rect.y-weapon.animate.y_offset)) 
    # Движение по X
    ball.rect.centerx += Vx
    Vx_flag = check_mask_collision(ball,cave,Vx,0)

    # Движение по Y
    ball.rect.centery += Vy 
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
