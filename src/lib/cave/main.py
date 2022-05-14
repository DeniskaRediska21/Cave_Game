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
        import itertools

        room = abs(room-1)

        image_out = Image.new(mode = '1', size = (l,h))
        pixels = list(itertools.chain(*room))
        image_out.putdata(pixels)
        image_out.save('cave.png')


# cave = Cave()
# cave.save_cave(47,80,60,1)