import pygame
import random

from lib.cave.main import Cave

l=80
h=60
cave = Cave()
cave.save_cave(47,l,h,1,10,smooth_pixels=False) #True для гладкой карты, False(Быстрее) для пиксельной

class combat(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.sprites.__init__(self.sprites)
        self.animate.__init__(self.animate)
        self.image = self.sprites.mining_hit_right[-1]
        self.rect = self.image.get_rect() # size and position
        self.w = self.rect.width
        self.h = self.rect.height

    def update(self,character):
        if self.animate.mining_hit_right:
            self.rect.bottomleft = character.rect.bottomright
        elif self.animate.mining_hit_left:
            self.rect.bottomright = character.rect.bottomleft

        if self.animate.mining_hit_right == True:
            self.animate.current_frame += 0.4
            if self.animate.current_frame >= len(self.sprites.mining_hit_right):
                self.animate.current_frame = 0
                self.animate.mining_hit_right = False
            self.image = self.sprites.mining_hit_right[int(self.animate.current_frame)]
            self.animate.Set_offsets(self)
            self.animate.y_offset = 0

        if self.animate.mining_hit_left == True:
            self.animate.current_frame += 0.4
            if self.animate.current_frame >= len(self.sprites.mining_hit_left):
                self.animate.current_frame = 0
                self.animate.mining_hit_left = False
            self.image = self.sprites.mining_hit_left[int(self.animate.current_frame)]
            self.animate.Set_offsets(self)
            self.animate.y_offset = 0

    class animate():
        def __init__(self):
            self.current_frame = 0
            self.x_offset = 0
            self.y_offset = 0
            
            self.mining_hit_right = False
            self.mining_hit_left = False

        def Set_offsets(self):
            self.animate.x_offset = (self.image.get_rect().width - self.w)/2
            self.animate.y_offset = (self.image.get_rect().height - self.h)

        def setup(self):
                self.current_frame = 0
                self.mining_hit_right = False
                self.mining_hit_left = False
                
        def Mining_hit_right(self):
            if not self.mining_hit_right:
                self.setup(self)
                self.mining_hit_right = True

        def Mining_hit_left(self):
            if not self.mining_hit_left:
                self.setup(self)
                self.mining_hit_left = True

    class sprites():
        def __init__(self):
            self.mining_hit_right = []
            self.mining_hit_left = []

            self.mining_hit_right.append(pygame.image.load("src\Textures\Mining_hit_r_1.png"))
            self.mining_hit_right.append(pygame.image.load("src\Textures\Mining_hit_r_2.png"))
            self.mining_hit_right.append(pygame.image.load("src\Textures\Mining_hit_r_3.png"))
            self.mining_hit_right.append(pygame.image.load("src\Textures\Mining_hit_r_4.png"))

            self.mining_hit_left.append(pygame.image.load("src\Textures\Mining_hit_l_1.png"))
            self.mining_hit_left.append(pygame.image.load("src\Textures\Mining_hit_l_2.png"))
            self.mining_hit_left.append(pygame.image.load("src\Textures\Mining_hit_l_3.png"))
            self.mining_hit_left.append(pygame.image.load("src\Textures\Mining_hit_l_4.png"))
        

class character(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.sprites.__init__(self.sprites)
        self.animate.__init__(self.animate)
        # self.sprites.static = []
        # self.sprites.static.append(pygame.image.load("src\Textures\Player.png")) 
        # self.sprites()

        self.image = self.sprites.static[0]
        self.rect = self.image.get_rect() # size and position
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.w = self.rect.width
        self.h = self.rect.height
        self.mask = pygame.mask.from_surface(self.image)

    
    def update(self):
        self.animate.x_offset = 0
        self.animate.y_offset = 0
        if self.animate.standing == True and self.animate.landed == False:
            self.animate.current_frame += 0.05
            if self.animate.current_frame >= len(self.sprites.static):
                self.animate.current_frame = 0
                self.animate.standing = False
            self.image = self.sprites.static[int(self.animate.current_frame)]
            self.animate.Set_offsets(self)

        if self.animate.walking_right == True:
            self.animate.current_frame += 0.2
            if self.animate.current_frame >= len(self.sprites.walking_right):
                self.animate.current_frame = 0
                self.animate.walking_right = False
            self.image = self.sprites.walking_right[int(self.animate.current_frame)]
            self.animate.Set_offsets(self)
            self.animate.x_offset = self.animate.x_offset*2

        if self.animate.walking_left == True:
            self.animate.current_frame += 0.2
            if self.animate.current_frame >= len(self.sprites.walking_left):
                self.animate.current_frame = 0
                self.animate.walking_left = False
            self.image = self.sprites.walking_left[int(self.animate.current_frame)]
            self.animate.Set_offsets(self)
            self.animate.x_offset = 0

        if self.animate.falling == True:
            self.animate.current_frame += 0.1
            if self.animate.current_frame >= len(self.sprites.falling):
                self.animate.current_frame = len(self.sprites.jumping)-1
                # self.animate.falling = False
            self.image = self.sprites.falling[int(self.animate.current_frame)]
            self.animate.Set_offsets(self)


        if self.animate.jumping == True:
            self.animate.current_frame += 0.1
            if self.animate.current_frame >= len(self.sprites.jumping):
                self.animate.current_frame = len(self.sprites.jumping)-1
                # self.animate.jumping = False
            self.image = self.sprites.jumping[int(self.animate.current_frame)]
            self.animate.Set_offsets(self)
            
        
        if self.animate.landed == True:
            self.animate.current_frame += 1
            if self.animate.current_frame >= len(self.sprites.landed):
                self.animate.current_frame = 0
                self.animate.landed = False
            self.image = self.sprites.landed[int(self.animate.current_frame)]
            self.animate.Set_offsets(self)
        
        



    class animate():
        def __init__(self):
            self.current_frame = 0
            self.x_offset = 0
            self.y_offset = 0
            self.walking_right = False
            self.walking_left = False
            self.jumping = False
            self.falling = False
            self.standing = False
            self.landed = False

        def Set_offsets(self):
            self.animate.x_offset = (self.image.get_rect().width - self.w)/2
            self.animate.y_offset = (self.image.get_rect().height - self.h)

        def setup(self):
                self.current_frame = 0
                self.walking_right = False
                self.walking_left = False
                self.jumping = False
                self.falling = False
                self.standing = False

        def Walking_right(self):
            if not self.walking_right:
                self.setup(self)
                self.walking_right = True
                self.landed = False
  
        def Walking_left(self):
            if not self.walking_left:
                self.setup(self)
                self.walking_left = True
                self.landed = False
        def Falling(self):
            if not self.falling:
                self.setup(self)
                self.falling = True
                self.landed = False
        def Jumping(self):
            if not self.jumping:
                self.setup(self)
                self.jumping = True
                self.landed = False
        def Standing(self):
            if not self.standing:
                self.setup(self)
                self.standing = True
        def Landed(self):
            if not self.landed:
                self.setup(self)
                self.landed = True

    class sprites():
        def __init__(self):
            self.static = []
            self.walking_right = []
            self.walking_left = []
            self.jumping = []
            self.falling = []
            self.landed = []
            self.static.append(pygame.image.load("src\Textures\Player_static_1.png"))
            self.static.append(pygame.image.load("src\Textures\Player_static_2.png"))
            self.static.append(pygame.image.load("src\Textures\Player_static_3.png"))

            self.walking_right.append(pygame.image.load("src\Textures\Player_walking_r_1.png"))
            self.walking_right.append(pygame.image.load("src\Textures\Player_walking_r_2.png"))

            self.walking_left.append(pygame.image.load("src\Textures\Player_walking_l_1.png"))
            self.walking_left.append(pygame.image.load("src\Textures\Player_walking_l_2.png"))

            self.jumping.append(pygame.image.load("src\Textures\Player_jumping_1.png"))
            self.jumping.append(pygame.image.load("src\Textures\Player_jumping_2.png"))

            self.falling.append(pygame.image.load("src\Textures\Player_falling_1.png"))
            self.falling.append(pygame.image.load("src\Textures\Player_falling_2.png"))

            self.landed.append(pygame.image.load("src\Textures\Player_landed_1.png"))
            self.landed.append(pygame.image.load("src\Textures\Player_landed_2.png"))
            self.landed.append(pygame.image.load("src\Textures\Player_landed_3.png"))

        
        


class map(pygame.sprite.Sprite):

    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)

        self.image = surface

        self.rect = self.image.get_rect() # size and position

        self.mask = pygame.mask.from_surface(self.image)

def check_ground(ball,map):
    onground = True
    ball.rect.bottom += 1
    if pygame.sprite.collide_mask(map,ball) == None:
        onground = False
    ball.rect.bottom -= 1
    
    return onground

def check_mask_collision(ball,map,Vx,Vy,slope_tolarance = 10):
    Flag = 0    
    if pygame.sprite.collide_mask(map,ball) != None:
        Flag = 4
        if Vx>0:
            for i in range(abs(Vx)):
                Flag = 3
                ball.rect.right -= 1
                for j in range(slope_tolarance):
                    ball.rect.bottom -= 1
                    if pygame.sprite.collide_mask(map,ball) == None:
                        return Flag
                ball.rect.bottom += slope_tolarance
                if pygame.sprite.collide_mask(map,ball) == None:
                    return Flag


        elif Vx<0:
            for i in range(abs(Vx)):
                Flag = 3
                ball.rect.left += 1
                for j in range(slope_tolarance):
                    ball.rect.bottom -= 1
                    if pygame.sprite.collide_mask(map,ball) == None:
                        return Flag
                ball.rect.bottom += slope_tolarance
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
# Высота прыжка
Vy0 = 15

Vx = 0
Vy = 0
# Максимальная скорость по X
Vx_max = 7
# Ускорение свободного падения
g = 1

cave = pygame.image.load("src\Textures\cave.png") 
cave = map(cave)


ball = character((0,0))
random_spawn(ball,cave)
weapon = combat((ball.rect.x,ball.rect.y))
# Группировка спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add(ball)
all_sprites.add(cave)

combat_sprites = pygame.sprite.Group()
combat_sprites.add(weapon)

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
    screen.blit(ball.image,(ball.rect.x-ball.animate.x_offset,ball.rect.y-ball.animate.y_offset))
    screen.blit(cave.image,cave.rect.topleft)
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
    
    combat_sprites.update(ball)


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
