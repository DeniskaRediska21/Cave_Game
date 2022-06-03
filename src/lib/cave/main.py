from ctypes import resize
from tkinter.filedialog import SaveAs
import numpy as np
import numpy.random as rand

class Cave:
    def smooth(self,room,step):
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


    def generate_random_room(self,fill_percent,l,h,step,smoothig_steps = 5):
        room = rand.rand(h,l)*100
        room[room>fill_percent]= 0
        room[room>0] = 1
        room[0,:] = 1
        room[-1,:] = 1
        room[:,0] = 1
        room[:,-1] = 1
        for i in range(smoothig_steps):
            room = self.smooth(room,step)
        return room


    def save_cave(self,fill_percent,l,h,step,scale,smooth_pixels = True,smoothig_steps = 5):
        # fill_percent = 47
        # h = 60
        # l = 80
        # step = 1
        room = self.generate_random_room(fill_percent,l,h,step,smoothig_steps)
        # print(room)

        from PIL import Image
        import itertools
        
        # Увеличение
        room = np.array(room).repeat(scale,axis=0).repeat(scale,axis=1) 

        # Сглаживание останков пикселей
        if smooth_pixels:
            room = self.smooth(room,scale//2)

        # Приведение в формат L
        room = room*255

        # Подсчет alpha канала
        alpha = room
        alpha[room == 255] = 255
        alpha[room == 0] = 0
        # Инферсия цвета, чтобы стены были черными
        room = abs(room-255)

        # PNG говны
        image_out = Image.new(mode = 'L', size = (l*scale,h*scale))
        image_alpha = Image.new(mode = 'L', size = (l*scale,h*scale))
        pixels = list(itertools.chain(*room))
        alpha = list(itertools.chain(*alpha))
        image_out.putdata(pixels)
        image_alpha.putdata(alpha)
        image_out.putalpha(image_alpha)
        image_out.save('src/Textures/cave.png')
        return room


# from PIL import Image
# import numpy as np
# import PIL
# import itertools
l=80
h=60
cave = Cave()
cave.save_cave(47,l,h,1,10,smooth_pixels=False)