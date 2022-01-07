import numpy as np
import matplotlib.pyplot as plt
import threading
import time

"""
This script updates the plot by clearing the existing
data in the axes. If the data is to large and changes
are minimal, need to consider another method to plot.
"""

class plotter():
    def __init__(self,fig,ax):
        self.fig = fig
        self.ax = ax
        self.data = np.zeros((30,30),dtype=np.int32)
        # self.dummy_fig()

    # def dummy_fig(self):
    #     self.fig2,self.ax2 = plt.subplots()
    #     self.fig2.set_size_inches(6, 12)
    #     self.ax2.axes.xaxis.set_visible(False)
    #     self.ax2.axes.yaxis.set_visible(False)
    #     self.ax2.imshow(self.data)
    #     plt.pause(0.01)

    def update_plot(self):
        self.ax.clear()
        self.ax.imshow(self.data)
        self.ax.set_xlim(0, 30)
        self.ax.set_ylim(0, 30)
        vertices = self.fig.ginput(n=-1,timeout=30)
        for vertex in vertices:
            self.data[int(round(vertex[1])),int(round(vertex[0]))] = 255
        # This will draw the updated artists on the figure
        # self.fig.canvas.draw()
        plt.pause(0.01)
        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        # self.fig.canvas.flush_events()

    def thread_function(self):
        while True:
            print("hey")
            #vertices = self.fig2.ginput(n=1,timeout=30)
            # print(vertices)
            # self.data[] = 
            time.sleep(5)


def main():
    fig,ax1 = plt.subplots()
    fig.set_size_inches(6, 12)
    ax1.axes.xaxis.set_visible(False)
    ax1.axes.yaxis.set_visible(False)
    drawing1 = plotter(fig,ax1)
    # This will enable the script to run even after plt.show()
    plt.ion()
    plt.axis('equal')
    # plt.suptitle("Plot Title",fontsize=22,y=0.94)
    
    # This will display the plot
    drawing1.update_plot()
    plt.pause(0.01)
    x = threading.Thread(target=drawing1.thread_function, args=())
    x.start()
    while True:
        drawing1.update_plot()


if __name__ == '__main__':
    main()

