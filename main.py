# Made by IcyMink Apr 2024

import noiseMap
import matplotlib.pyplot as plt


def main():
    height = 16
    width = 16
    resolution = 0.01
    interp_method = 2

    pm = noiseMap.get_perlin_map(height, width, resolution, interp_method)

    plt.imshow(pm, cmap='hot', interpolation='nearest')
    plt.show()


if __name__ == "__main__":
    main()
