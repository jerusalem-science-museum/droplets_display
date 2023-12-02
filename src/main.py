from multiprocessing import Process

from droplets_player import DropletsPlayer
from droplets_simulator import DropletsSimulator


def main():
    ds = DropletsSimulator()
    dp = DropletsPlayer(ds)
    p = Process(target=ds.animate)
    p.start()
    # dp.play_rain()
    dp.play_vox()
    p.join()


if __name__ == '__main__':
    main()
