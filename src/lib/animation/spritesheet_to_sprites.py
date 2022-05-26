import pygame
import numpy as np
def sheet2frames(file):
    spritesheet = pygame.image.load(file)
    spritesheet.set_colorkey((255, 255, 255, 255))

    length = len(spritesheet.get_at((0,0)))-1
    sections = []
    size = spritesheet.get_size()
    colorkey = spritesheet.get_colorkey()

    for i in range(max(size)):
        current_colomn = 0
        for j in range(min(size)):
            current_pixel = spritesheet.get_at((i,j))
            if not current_pixel == colorkey:
                current_colomn = max(current_colomn,current_pixel[length])

        sections.append(current_colomn)

    sections.append(0)

    beginings = []
    ends = []

    prev_collumn = 0
    for number,collumn in enumerate(sections):
        if prev_collumn == 0 and collumn !=0:
            beginings.append(number)
        elif prev_collumn!=0 and collumn == 0:
            ends.append(number-1)
        prev_collumn = collumn

    lengths = np.array(ends)-np.array(beginings)

    heights = np.zeros_like(lengths)
    for number, begining in enumerate(beginings):
        for j in range(ends[number] - begining+1):
            current_height = 0
            for i in range(min(size)):
                current_pixel = spritesheet.get_at((begining + j,i))
                if not current_pixel == colorkey and current_pixel[length] != 0:
                    current_height += 1
            heights[number] = max(heights[number], current_height)

    RECT_WIDTH = max(lengths)
    # RECT_HIEGHT = min(size)
    frames = []
    for number,begining in enumerate(beginings):
        selection_window = (pygame.Rect(begining,0,lengths[number]+1,heights[number]))
        selection_window.bottom = max(heights)
        frames.append(spritesheet.subsurface(selection_window))
    return frames

# frames = sheet2frames('src\Textures\Player_static.png')
# WIDTH = 200
# HEIGHT = 200
# FPS = 30
#
# # Создаем игру и окно
# pygame.init()
# pygame.mixer.init()
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("My Game")
# clock = pygame.time.Clock()
# n_frame = 0
# running = True
# while running:
#     screen.fill((127,127,127))
#
#     screen.blit(frames[n_frame],(100,100))
#     for event in pygame.event.get():
#         # check for closing window
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 n_frame +=1
#                 if n_frame >= len(frames):
#                     n_frame = 0
#     clock.tick(FPS)
#     pygame.display.flip()
#
# pygame.quit()