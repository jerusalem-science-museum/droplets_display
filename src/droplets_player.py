#!/usr/bin/python3

import numpy as np
from time import sleep
from midvoxio.voxio import get_vox, plot_3d
import constants as C
import matplotlib.pyplot as plt
from multiprocessing import Process

class DropletsPlayer:
    def __init__(self, ds) -> None:
        self.ds = ds
        self.vox_files = [f for f in C.RES_PATH.iterdir() if f.is_file()]

    def send_droplets(self, z_slice) -> None:
        self.ds.add_data(np.array(np.nonzero(z_slice)))

    def show_voxs(self) -> None:
        axs = []
        for vox_file in self.vox_files:
            vox = get_vox(vox_file)
            for vox_index in range(max(len(vox.nshps), 1)):
                # plot_3d(vox.to_list(vox_index))
                Process(target=plot_3d, args=(vox.to_list(vox_index),)).start()
                # vox_arr = vox.to_list(vox_index)
                # axs.append(plt.subplot(111, projection='3d'))
                # u = np.moveaxis(vox_arr, (0, 1), (0, 1))
                # m = axs[-1].voxels((u[:, :, :, 3] > 0.1), facecolors=np.clip(u[:, :, :, :4], 0, 1))
        # p = Process(target=plt.show)
        # p.start()
        # p.join()

    def play_vox(self) -> None:
        # self.show_voxs()
        while True:
            for vox_file in self.vox_files:
                vox = get_vox(vox_file)
                for vox_index in range(max(len(vox.nshps), 1)):
                    l, w, h = vox.sizes[vox_index]
                    z_slices = np.zeros((h, l, w))
                    print(vox_file.name, l, w, h)
                    for (x, y, z, c) in vox.voxels[vox_index]:
                        z_slices[z][x][y] = c

                    for z_slice in z_slices:
                        self.send_droplets(z_slice)
                        sleep(0.07)

                    sleep(8)

    def play_rain(self) -> None:
        while True:
            self.ds.add_data(np.random.randint([[C.X_SIZE], [C.Y_SIZE]], size=(2, 10)))
            sleep(1)


def main():
    dp = DropletsPlayer()
    dp.loop_play(print)


if __name__ == '__main__':
    main()
