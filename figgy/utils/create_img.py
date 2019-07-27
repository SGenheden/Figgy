import os

import matplotlib.pylab as plt
import numpy as np

from figgy.game_logic import Block


def main(color, name):
    color = np.asarray(color)
    alt_color = np.ones(3) - color / 2
    fig = plt.figure(figsize=(Block.block_size, Block.block_size), dpi=1)
    mat = np.zeros((Block.block_size, Block.block_size, 3))
    mat[:, :] = [0.7, 0.7, 0.7]
    mat[1:-1, 1:-1] = alt_color
    mat[2:-2, 2:-2] = color
    fig.gca().axis("off")
    fig.gca().imshow(mat, extent=(0, Block.block_size, 0, Block.block_size))
    fig.tight_layout()
    this_path = os.path.dirname(os.path.abspath(__file__))
    fig.savefig(os.path.join(this_path, "..", "images", f"{name}.png"), pad_inches=0)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Create images for the Figgy game")
    parser.add_argument(
        "--color",
        nargs=3,
        type=float,
        default=[0, 1.0, 0.0],
        help="Specify the RGB colors in ranges from 0 to 1",
    )
    parser.add_argument(
        "--name", default="unnamed", help="Specify the name of the image"
    )
    parser.add_argument("--colormap", help="Produce images from a color map")
    args = parser.parse_args()

    if args.colormap:
        cmap = plt.get_cmap(args.colormap)
        for i, color in enumerate(cmap.colors):
            name = f"{args.colormap.lower()}_{i}"
            main(color=list(color), name=name)
    else:
        main(color=args.color, name=args.name)
