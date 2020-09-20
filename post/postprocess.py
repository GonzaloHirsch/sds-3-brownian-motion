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
VELOCITY_PROBABILITY = "vp"
TRAJECTORY_ONE = "tro"
TRAJECTORY_MULTIPLE = "trm"

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

    weights = np.ones_like(collision_timespans) / len(collision_timespans)

    p = plt.hist(collision_timespans, bins=np.arange(min(collision_timespans), max(collision_timespans) + 0.0005, 0.0005), weights=weights)
    plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
    plt.gca().xaxis.set_minor_locator(MultipleLocator(0.0005))
    plt.show()


def compute_velocity_probability(filename):
    f = open(filename, 'r')

    velocity_modules = []

    current_time = 0
    time = 0
    for line in f:
        data = line.rstrip("\n").split(" ")
        if len(data) == 1:
            # Saving the last time to know the length of the simulation
            time = float(data[0])

    # Getting the last third of the time of the simulation
    time = time * (2/3)

    f.close()
    f = open(filename, 'r')

    for line in f:
        data = line.rstrip("\n").split(" ")
        if len(data) == 1:
            current_time = float(data[0])
        if len(data) > 1:
            if current_time > time:
                x_velocity = float(data[2])
                y_velocity = float(data[3])
                velocity_modules.append((x_velocity**2 + y_velocity**2)**(1/2))
    f.close()

    weights = np.ones_like(velocity_modules) / len(velocity_modules)
    plt.hist(velocity_modules, bins=np.arange(min(velocity_modules), max(velocity_modules) + 0.25, 0.25), weights=weights)
    plt.gca().xaxis.set_minor_locator(MultipleLocator(0.25))
    plt.show()

def compute_velocity_probability_at_t0(filename):
    f = open(filename, 'r')

    velocity_modules = []
    time = -1

    for line in f:
        data = line.rstrip("\n").split(" ")
        if len(data) == 1:
            if time >= 0:
                break
            time = float(data[0])
        if len(data) > 1:
            x_velocity = float(data[2])
            y_velocity = float(data[3])
            velocity_modules.append((x_velocity**2 + y_velocity**2)**(1/2))

    f.close()

    weights = np.ones_like(velocity_modules) / len(velocity_modules)
    plt.hist(velocity_modules, bins=np.arange(min(velocity_modules), max(velocity_modules) + 0.25, 0.25), weights=weights)
    plt.gca().xaxis.set_minor_locator(MultipleLocator(0.25))
    plt.show()



def compute_trajectory_one(dynamic_filename, static_filename):
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

def compute_trajectory_multiple(dynamic_filename, dynamic_slower_filename, dynamic_faster_filename, static_filename):
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

    f = open(dynamic_slower_filename, 'r')

    points_x_slower = []
    points_y_slower = []

    isFirst = True

    for line in f:
        data = line.rstrip("\n").split(" ")
        if len(data) == 1:
            current_time = float(data[0])
            isFirst = True
        else:
            if isFirst:
                isFirst = False
                points_x_slower.append(float(data[0]))
                points_y_slower.append(float(data[1]))

    f.close()

    f = open(dynamic_faster_filename, 'r')

    points_x_faster = []
    points_y_faster = []

    isFirst = True

    for line in f:
        data = line.rstrip("\n").split(" ")
        if len(data) == 1:
            current_time = float(data[0])
            isFirst = True
        else:
            if isFirst:
                isFirst = False
                points_x_faster.append(float(data[0]))
                points_y_faster.append(float(data[1]))

    f.close()

    plt.plot(points_x, points_y, 'r', label = "Trayectoria Normal")
    plt.plot(points_x_slower, points_y_slower, 'g', label = "Trayectoria con menos Velocidad")
    plt.plot(points_x_faster, points_y_faster, 'b', label = "Trayectoria con más Velocidad")
    plt.plot(points_x[0], points_y[0], 'go', label = "Inicio")
    plt.plot(points_x[-1], points_y[-1], 'ko', label = "Fin Normal")
    plt.plot(points_x_slower[-1], points_y_slower[-1], 'kx', label = "Fin con menos Velocidad")
    plt.plot(points_x_faster[-1], points_y_faster[-1], 'k*', label = "Fin con más Velocidad")
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
    elif args.process_type == TRAJECTORY_ONE:
        print("Computing trajectory...")
        compute_trajectory_one('./parsable_files/dynamic.txt', './parsable_files/static.txt')
    elif args.process_type == TRAJECTORY_MULTIPLE:
        print("Computing trajectory...")
        compute_trajectory_multiple('./parsable_files/dynamic.txt', './parsable_files/dynamic_slower.txt',  './parsable_files/dynamic_faster.txt', './parsable_files/static.txt')
    elif args.process_type == VELOCITY_PROBABILITY:
        print("Computing velocity probability...")
        compute_velocity_probability('./parsable_files/dynamic.txt')


# call main
if __name__ == '__main__':
    main()

