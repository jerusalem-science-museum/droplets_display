#!/usr/bin/python3

from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist
from multiprocessing import Queue


class DropletsSimulator:
    # Gravitational acceleration on earth in m*s^-2
    _Z_ACCELERATION = 9.80665

    def __init__(
        self,
        initial_z_velocity: float = 1,
        x_size: int = 64,
        y_size: int = 32,
        z_size: int = 50,
        interval: float = 0.001,
        initial_view: tuple[float, float, float] = (10, -80, 0),
    ) -> None:
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.fig.tight_layout()
        self.initial_z_velocity = -initial_z_velocity
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
        self.interval = interval
        self._queue = Queue()

        self.ax.set_xlim(0, self.x_size)
        self.ax.set_ylim(0, self.y_size)
        self.ax.set_zlim(0, self.z_size)
        self.ax.view_init(*initial_view)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])

        self.data = np.zeros((3, 0), dtype=float)
        self.velocities = np.full(self.data.shape[1], fill_value=self.initial_z_velocity, dtype=float)

        self.scatter = self.ax.scatter(*self.data, color="blue", animated=True)

    def _update(self, _current_frame: float) -> list[Artist]:
        if not self._queue.empty():
            self._add_data(self._queue.get())

        self.velocities -= self._Z_ACCELERATION * self.interval
        self.data[2] += self.velocities
        mask = self.data[2] > 0
        self.velocities = self.velocities[mask]
        self.data = self.data[:, mask]
        self.scatter._offsets3d = self.data
        return [self.ax, self.scatter]

    def _add_data(self, xy: np.ndarray[tuple[Literal[2], int], np.dtype[np.int_]]) -> None:
        self.data = np.hstack((self.data, np.vstack((xy, np.full(xy.shape[1], fill_value=self.z_size)))))
        self.velocities = np.hstack((self.velocities, np.full(xy.shape[1], fill_value=self.initial_z_velocity)))

    def add_data(self, xy: np.ndarray[tuple[Literal[2], int], np.dtype[np.int_]]) -> None:
        self._queue.put(xy)

    def animate(self, block: bool = True) -> None:
        _ani = FuncAnimation(
            self.fig,
            self._update,
            interval=self.interval,
            blit=True,
            repeat=False,
        )
        self.fig.canvas.manager.window.raise_()
        plt.show(block=block)
        plt.close()


def main():
    ds = DropletsSimulator()
    ds.add_data(np.random.randint([[ds.x_size], [ds.y_size]], size=(2, 10)))
    ds.animate()


if __name__ == '__main__':
    main()
