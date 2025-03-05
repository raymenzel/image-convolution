#!/bin/bash -e

test_directory=$(realpath "$(dirname "${BASH_SOURCE[0]}")")
dataset1="$test_directory/convolve_raw_0.dat"
dataset2="$test_directory/convolve_raw_1.dat"
output="out.png"

# Run the application.
image-convolver $dataset1 $dataset2 $output
if [ "$?" -ne "0" ]; then
  echo "Error: image-convolver failed."
  exit 1
fi

if [ ! -f "${dataset1}.png" ]; then
    echo "Error: failed to generate an image for the first input dataset."
    exit 1
fi

if [ ! -f "${dataset2}.png" ]; then
    echo "Error: failed to generate an image for the second input dataset."
    exit 1
fi

if [ ! -f "$output" ]; then
    echo "Error: failed to generate the convolved output image."
    exit 1
fi
