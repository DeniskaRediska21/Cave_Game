from ctypes import resize
from tkinter.filedialog import SaveAs
import numpy as np
import numpy.random as rand

class Cave:
    def save_cave(self,fill_percent,l,h,step):
        def generate_random_room(fill_percent,l,h,step):
            def smooth(room,step):
                h,l = np.shape(room)
                neibours = np.ones((h,l))*((step*2+1)**2-1)

                for i in range(step,h-step):
                    for j in range(step,l-step):
                        neibours[i,j] = np.sum(np.sum(room[i-step:i+step+1,j-step:j+step+1]))
                        neibours[i,j] -= room[i,j]

                treshold = ((step*2+1)**2-1)/2
                room[neibours>treshold] = 1
                room[neibours<treshold] = 0
                return room


            room = rand.rand(h,l)*100
            room[room>fill_percent]= 0
            room[room>0] = 1
            room[0,:] = 1
            room[-1,:] = 1
            room[:,0] = 1
            room[:,-1] = 1
            for i in range(5):
                room = smooth(room,step)
            return room
        # fill_percent = 47
        # h = 60
        # l = 80
        # step = 1
        room = generate_random_room(fill_percent,l,h,step)
        # print(room)

        from PIL import Image
        from PIL import ImageDraw
        import itertools

        # Приведение в формат L
        room = room*255

        # Подсчет alpha канала
        alpha = room
        alpha[room == 255] = 255
        alpha[room == 0] = 0
        # Инферсия цвета, чтобы стены были черными
        room = abs(room-255)

        image_out = Image.new(mode = 'L', size = (l,h))
        image_alpha = Image.new(mode = 'L', size = (l,h))
        pixels = list(itertools.chain(*room))
        alpha = list(itertools.chain(*alpha))
        image_out.putdata(pixels)
        image_alpha.putdata(alpha)
        image_out.putalpha(image_alpha)
        image_out.save('cave.png')
        return room



# cave = Cave()
# room = cave.save_cave(47,80,60,1)

