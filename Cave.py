import numpy as np
import numpy.random as rand

class Cave:
    def generate_random_room(self,fill_percent,l,h,step):


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

# import matplotlib.pyplot as plt

# fill_percent = 47
# h = 60
# l = 80
# step = 1

# cave = Cave()
# room = cave.generate_random_room(fill_percent,l,h,step)

# fig, ax = plt.subplots()
# ax.imshow(room)
# plt.show()