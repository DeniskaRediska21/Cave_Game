import pygame
import random
from lib.colisions.colisions import check_mask_collision

class map(pygame.sprite.Sprite):

    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)

        self.image = surface

        self.rect = self.image.get_rect() # size and position

        self.mask = pygame.mask.from_surface(self.image)



def random_spawn(ball,cave):
    ball.rect.x = round(random.random() * cave.rect.width)
    ball.rect.y = round(random.random() * cave.rect.height)
    while check_mask_collision(ball,cave,0,0,0) != 0:
        ball.rect.x = round(random.random() * cave.rect.width)
        ball.rect.y = round(random.random() * cave.rect.height)