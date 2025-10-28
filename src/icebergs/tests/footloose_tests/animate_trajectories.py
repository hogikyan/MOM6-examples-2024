#!/usr/bin/env python

from netCDF4 import Dataset
import pdb
import netCDF4 as nc
import numpy as np
import matplotlib
import math
import os
matplotlib.use("tkagg")
from pylab import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1 import make_axes_locatable
import argparse

def parseCommandLine():
    parser = argparse.ArgumentParser(description=
    '''Generate animation of iceberg trajectories.''',
    epilog='Written by Alex Huth, 2020')
    parser.add_argument('-fname', type=str, default='iceberg_trajectories.nc',
                    help=''' provide filename to plot''')
    parser.add_argument('-s', type=int, default='1450',
                        help='''plotted particle size''')
    optCmdLineArgs = parser.parse_args()
    return optCmdLineArgs



def main(args):

    print('reading file')

    filename=args.fname
    psize=args.s
    #filename = 'iceberg_trajectories.nc'
    field = 'lon'
    field2 = 'lat'

    with nc.Dataset(filename) as file:
        x = file.variables['lon'][:]/1.e3
        y = file.variables['lat'][:]/1.e3
        day = file.variables['day'][:]
        bid = file.variables['id_ij'][:]
        vo = file.variables['fl_k'][:]
        length = file.variables['length'][:]
        width = file.variables['width'][:]

    ud = np.unique(day)
    ub = np.unique(bid)
    t = ud[0]

    radius = length*width*(1./(2*np.sqrt(3)))

    urad=np.unique(radius)
    #print('urad',urad)

    # frame info
    num_frames = len(ud)
    movie_len = 10.0 #seconds
    frame_len = 1000.0*movie_len/num_frames

    xmin = 0 #np.floor(min(min(x),min(y),0))
    xmax = 20 #np.ceil(max(max(x),max(y),20))
    ymin = xmin
    ymax = xmax

    anim_running = True

    def animate(i):

        x1 = x[day == ud[i]]
        y1 = y[day == ud[i]]
        data = np.hstack((x1[:,np.newaxis],y1[:,np.newaxis]))

        scat.set_offsets(data)

        vo1 = vo[day == ud[i]]
        scat.set_edgecolor('k')
        scat.set_color(cmap(norm(vo1)))

        r1 = radius[day == ud[i]]
        scat.set_sizes(r1/psize)

        t = ud[i]
        time_text.set_text('time = %.1f days' % t )
        return scat,time_text

    def init():
        scat.set_offsets([])
        return scat,

    def onClick(event):
        global anim_running
        if anim_running:
            ani.event_source.stop()
            anim_running = False
        else:
            ani.event_source.start()
            anim_running = True

    # Now we can do the plotting!
    f = plt.figure(figsize=(5,5))
    f.tight_layout()
    ax1 = plt.subplot(111,xlim=(xmin, xmax), ylim=(ymin, ymax))
    div = make_axes_locatable(ax1)
    cax = div.append_axes('right', '5%', '5%')
    scat = ax1.scatter([],[],marker='o')
    time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes)

    cmap = plt.cm.get_cmap('RdYlBu')
    norm = plt.Normalize(vo.min(), vo.max())
    cb1 = matplotlib.colorbar.ColorbarBase(cax, cmap=cmap,
                                           norm=norm,
                                           orientation='vertical')


    # Change major ticks to show every 20.
    ax1.xaxis.set_major_locator(MultipleLocator(5))
    ax1.yaxis.set_major_locator(MultipleLocator(5))

    ax1.xaxis.set_minor_locator(MultipleLocator(1))
    ax1.yaxis.set_minor_locator(MultipleLocator(1))

    # Turn grid on for both major and minor ticks and style minor slightly
    # differently.
    ax1.grid(which='major', color='#CCCCCC', linestyle=':')
    ax1.grid(which='minor', color='#CCCCCC', linestyle=':')

    ax1.set_xlabel('x (km)')
    ax1.set_ylabel('y (km)')
    ax1.set_title('Iceberg trajectory')

    f.canvas.mpl_connect('button_press_event', onClick)

    ani = FuncAnimation(
        f,animate,init_func=init,frames=num_frames,
        interval=frame_len,blit=True,repeat=True)

    print('time',t)

    plt.show()
    #animation.save("iceberg_traj_animation.mp4")


print('Script complete')

if __name__ == '__main__':
    optCmdLineArgs=	parseCommandLine()
    anim_running = True
    main(optCmdLineArgs)
