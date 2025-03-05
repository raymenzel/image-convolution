"""2D Convolution for input 2D datasets."""

from argparse import ArgumentParser

import matplotlib.pyplot as plt
from numpy import asarray, linspace, zeros
from scipy.signal import convolve2d


def load_dataset(path):
    """Read data out of a dataset and put it into a matrix.

    Args:
        path: Path to the dataset.

    Returns:
        Numpy 1D arrays of x values and y values and a numpy 2D
        array of data values.
    """
    x_values = set()
    y_values = set()

    # Read in the x and y domains.
    with open(path) as dataset:
        for line in dataset:
            x, y, z = line.split()
            x_values.add(x)
            y_values.add(y)

    # Convert from strings to floats.
    x_values = [float(x) for x in x_values]
    y_values = [float(y) for y in y_values]

    # Sort the arrays.
    x_values = asarray([x for x in sorted(x_values)])
    y_values = asarray([y for y in sorted(y_values)])

    # Read in the data and place it into the correct indices.
    x_lookup = {x: i for i, x in enumerate(x_values)}
    y_lookup = {y: i for i, y in enumerate(y_values)}
    data = zeros((y_values.size, x_values.size))
    with open(path) as dataset:
        for line in dataset:
            x, y, z = line.split()
            i = x_lookup[float(x)]
            j = y_lookup[float(y)]
            data[j, i] = float(z)
    return x_values, y_values, data


def plot_data(data, path, x=None, y=None):
    """Plots the data and saves it to an output file.

    Args:
        data: Numpy 2D array of data values.
        path: Path to output image.
        x: Numpy 1D array of x values.
        y: Numpy 1D array of y values.
    """
    # Plot the data.
    plt.cla()
    fig, ax = plt.subplots()
    if x is None or y is None:
        plt.imshow(data, origin="lower", aspect="auto")
        ax.set_axis_off()
    else:
        plt.imshow(data, origin="lower", aspect="auto",
                   extent=[x[0], x[-1], y[0], y[-1]])
        plt.xlabel("x")
        plt.ylabel("y")
    plt.savefig(path, format="png")
    plt.cla()


def cli():
    """Entry point for the image-convolver command line tool."""
    parser = ArgumentParser(description="Performs a 2D convolution of two datasets.")
    parser.add_argument("dataset1", help="A dataset.")
    parser.add_argument("dataset2", help="Another dataset.")
    parser.add_argument("output", help="Path to the output png file.")
    args = parser.parse_args()

    # Process and plot the first dataset."
    x1, y1, z1 = load_dataset(args.dataset1)
    plot_data(z1, f"{args.dataset1}.png", x1, y1)

    # Process and plot the second dataset."
    x2, y2, z2 = load_dataset(args.dataset2)
    plot_data(z2, f"{args.dataset2}.png", x2, y2)

    # Convolve the two images.
    result = convolve2d(z1, z2)
    plot_data(result, f"{args.output}")
