import pygame
from lib.animation.spritesheet_to_sprites import sheet2frames
from lib.colisions.colisions import check_mask_collision

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
        # Настройки движения
        self.Vx_acceleration = 3
        self.Vx_deceliration = 4
        # Высота прыжка
        self.Vy_jump = 15

        self.Vx = 0
        self.Vy = 0
        # Максимальная скорость по X
        self.Vx_max = 7
        # Ускорение свободного падения
        self.g = 1
        
        self.Jump_flag = True
        self.onground_prev = False
        self.onground = False

    def jump(self):
        if self.Jump_flag:
            self.Vy = -self.Vy_jump
            self.Jump_flag = False
    
    def accelerate_right(self):
        self.Vx = min(self.Vx+self.Vx_acceleration,self.Vx_max)   
    
    def accelerate_left(self):
        self.Vx = max(self.Vx-self.Vx_acceleration,-self.Vx_max)
        
    def decelerate(self):
        if self.Vx>0:
            self.Vx = max(0,self.Vx-self.Vx_deceliration)
        else:
            self.Vx = min(0,self.Vx+self.Vx_deceliration)
           
    def update(self,cave):
        self.rect.centerx += self.Vx
        Vx_flag = check_mask_collision(self,cave,self.Vx,0)

        # Движение по Y
        self.rect.centery += self.Vy 
        Vy_flag = check_mask_collision(self,cave,0,self.Vy)

        # Если ударисля о пол или потолок
        if Vy_flag == 1:
            self.Vy = 0
        elif Vy_flag == 2:
            self.Vy = 0
            self.Jump_flag = True

        # Гравитация
        self.Vy +=self.g 
        
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
            # timings.standing = 0.05
            # timings.walking_right = 0.2
            # timings.walking_left = 0.2
            # timings.jumping = 0.1
            # timings.falling = 0.1
            # timings.landed = 1

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
            # self.static.append(pygame.image.load("src\Textures\Player_static_1.png"))
            # self.static.append(pygame.image.load("src\Textures\Player_static_2.png"))
            # self.static.append(pygame.image.load("src\Textures\Player_static_3.png"))
            self.static = sheet2frames('src\Textures\Player_static.png')

            self.walking_right.append(pygame.image.load("src\Textures\Player_walking_r_1.png"))
            self.walking_right.append(pygame.image.load("src\Textures\Player_walking_r_2.png"))

            # Движение налево обратно движению направо
            for frame in self.walking_right:
                self.walking_left.append(pygame.transform.flip(frame, True, False))

            self.jumping.append(pygame.image.load("src\Textures\Player_jumping_1.png"))
            self.jumping.append(pygame.image.load("src\Textures\Player_jumping_2.png"))

            self.falling.append(pygame.image.load("src\Textures\Player_falling_1.png"))
            self.falling.append(pygame.image.load("src\Textures\Player_falling_2.png"))

            self.landed.append(pygame.image.load("src\Textures\Player_landed_1.png"))
            self.landed.append(pygame.image.load("src\Textures\Player_landed_2.png"))
            self.landed.append(pygame.image.load("src\Textures\Player_landed_3.png"))

 