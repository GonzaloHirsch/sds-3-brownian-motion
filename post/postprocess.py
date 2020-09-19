import numpy as np
import math
import argparse
import random as rnd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

# Usage examples
# python3 post/postprocess.py -t cf
# python3 post/postprocess.py -t cp

COLLISION_FREQUENCY = "cf"
COLLISION_PROBABILITY = "cp"
TRAJECTORY = "tr"

def compute_collision_frequency(filename, outfilename):
    f = open(filename, 'r')

    current_time = 0
    total_collisions = 0
    total_particles = 0
    has_total_particles = False

    for line in f:
        data = line.rstrip("\n").split(" ")
        if len(data) == 1:
            current_time = float(data[0])
            if total_collisions > 0:
                has_total_particles = True
            total_collisions += 1
        else:
            if not has_total_particles:
                total_particles += 1

    f.close()

    wf = open(outfilename, 'a')

    frequency = int(total_collisions / current_time)

    wf.write('{} {}\n'.format(total_particles, frequency))

    wf.close()

def compute_collision_probability(filename, outfilename):
    f = open(filename, 'r')

    collision_times = []
    collision_timespans = []

    for line in f:
        data = line.rstrip("\n").split(" ")
        if len(data) == 1:
            current_time = float(data[0])
            collision_times.append(current_time)

    f.close()

    index = 0

    for time in collision_times:
        if index > 0:
            collision_timespans.append(collision_times[index] - collision_times[index - 1])
        index += 1

    sum = 0

    for timespan in collision_timespans:
        sum += timespan

    span_average = sum/len(collision_timespans)

    print("THE AVERAGE TIMESPAN IS", span_average)

    truncated_spans = [round(x, 4) for x in collision_timespans]

    print("MIN", min(truncated_spans), "MAX", max(truncated_spans))

    plt.hist(truncated_spans, bins=np.arange(min(truncated_spans), max(truncated_spans) + 0.0005, 0.0005))
    plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
    plt.gca().xaxis.set_minor_locator(MultipleLocator(0.0005))
    plt.show()

def compute_trajectory(dynamic_filename, static_filename):
    f = open(dynamic_filename, 'r')

    points_x = []
    points_y = []

    isFirst = True

    for line in f:
        data = line.rstrip("\n").split(" ")
        if len(data) == 1:
            current_time = float(data[0])
            isFirst = True
        else:
            if isFirst:
                isFirst = False
                points_x.append(float(data[0]))
                points_y.append(float(data[1]))

    f.close()

    f = open(static_filename, 'r')

    area_length = 0
    radius = 0
    index = 0

    for line in f:
        data = line.rstrip("\n").split(" ")
        if index == 0:
            area_length = float(data[0])
        elif index == 1:
            radius = float(data[1])
            break
        index += 1

    f.close()

    plt.plot(points_x, points_y, 'r', label = "Trayectoria")
    plt.plot(points_x[0], points_y[0], 'go', label = "Inicio")
    plt.plot(points_x[-1], points_y[-1], 'ko', label = "Fin")
    plt.legend()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().xaxis.set_minor_locator(MultipleLocator(0.1))
    plt.gca().yaxis.set_minor_locator(MultipleLocator(0.1))
    plt.gca().set_xlabel('Posición X')
    plt.gca().set_ylabel('Posición Y')
    plt.xlim(radius, area_length - radius)
    plt.ylim(radius, area_length - radius)
    plt.show()

# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Post processing for the points data to generate data statistics")

    # add arguments
    parser.add_argument('-t', dest='process_type', required=True)
    args = parser.parse_args()

    # The possible types are
    # cf -> collision frequency

    if args.process_type == COLLISION_FREQUENCY:
        print("Computing collision frquency...")
        compute_collision_frequency('./parsable_files/dynamic.txt', './parsable_files/collision_frequency.txt')
    elif args.process_type == COLLISION_PROBABILITY:
        print("Computing collision probability...")
        compute_collision_probability('./parsable_files/dynamic.txt', './parsable_files/collision_frequency.txt')
    elif args.process_type == TRAJECTORY:
        print("Computing trajectory...")
        compute_trajectory('./parsable_files/dynamic.txt', './parsable_files/static.txt')


# call main
if __name__ == '__main__':
    main()

