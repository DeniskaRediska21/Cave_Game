import pygame
from lib.animation.spritesheet_to_sprites import sheet2frames

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
            # self.static = sheet2frames('src\Textures\Player_static_1.png')

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

 