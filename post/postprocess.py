import numpy as np
import math
import argparse
import random as rnd
import statistics
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

# Usage examples
# python3 post/postprocess.py -t cf
# python3 post/postprocess.py -t cp

COLLISION_FREQUENCY = "cf"
COLLISION_FREQUENCY_MEDIAN = "cfm"
COMPUTE_COLLISION_PROBABILITY = "ccp"
EXTRACT_COLLISION_PROBABILITY = "ecp"
COMPUTE_VELOCITY_PROBABILITY = "cvp"
EXTRACT_VELOCITY_PROBABILITY = "evp"
COMPUTE_VELOCITY_PROBABILITY_T0 = "cvp0"
EXTRACT_VELOCITY_PROBABILITY_T0 = "evp0"
TRAJECTORY_ONE = "tro"
TRAJECTORY_MULTIPLE = "trm"
MSD_B = "msdb"
MSD_S = "msds"
MSD_GRAPH = "msdg"

IMAGES = 'images/'

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

def compute_collision_frequency_median(filename):
    f = open(filename, 'r')

    frequency_data = {}

    for line in f:
        data = line.rstrip("\n").split(" ")
        n = int(data[0])
        count = int(data[1])
        if not n in frequency_data:
            frequency_data[n] = []
        frequency_data[n].append(count)

    f.close()

    for k in frequency_data:
        mean = statistics.mean(frequency_data[k])
        std = statistics.stdev(frequency_data[k], mean)
        print('Data for {} particles is MEAN = {} and STDEV = {}'.format(k, mean, std))

def extract_collision_probability(filename, outfilename):
    f = open(filename, 'r')

    collision_times = []
    collision_timespans = []

    count = 0
    has_count = False

    for line in f:
        data = line.rstrip("\n").split(" ")
        if len(data) == 1:
            current_time = float(data[0])
            collision_times.append(current_time)
            if count > 0:
                has_count = True
        else:
            if not has_count:
                count += 1

    f.close()

    index = 0

    for time in collision_times:
        if index > 0:
            collision_timespans.append(collision_times[index] - collision_times[index - 1])
        index += 1

    f = open(outfilename, 'a+')

    f.write(str(count))

    for span in collision_timespans:
        f.write(' {}'.format(span))

    f.write('\n')

    f.close()

def compute_collision_probability(filename):
    f = open(filename, 'r')

    spans = {}

    for line in f:
        data = line.rstrip("\n").split(" ")
        if not int(data[0]) in spans:
            spans[int(data[0])] = []
        times = [float(x) for x in data[1:]]
        for time in times:
            spans[int(data[0])].append(time)

    f.close()

    for key in spans:
        collision_timespans = spans[key]
        mean = statistics.mean(collision_timespans)
        std = statistics.stdev(collision_timespans, mean)
        print('Collision timespans for particles is MEAN = {} and STDEV = {}'.format(mean, std))

        weights = np.ones_like(collision_timespans) / len(collision_timespans)

        if key > 100:
            multiplier = 0.0005
            formatter = '%.4f'
        else:
            multiplier = 0.0025
            formatter = '%.2f'

        p = plt.hist(collision_timespans, bins=np.arange(min(collision_timespans), max(collision_timespans) + multiplier, multiplier), weights=weights)
        plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter(formatter))
        plt.gca().xaxis.set_minor_locator(MultipleLocator(multiplier))
        plt.gca().set_xlabel('Tiempo entre colisiones (s)')
        plt.gca().set_ylabel('Probabilidad de colisión')
        plt.show()

def compute_max_time(filename):
    f = open(filename, 'r')

    time = 0
    for line in f:
        data = line.rstrip("\n").split(" ")
        if len(data) == 1:
            # Saving the last time to know the length of the simulation
            time = float(data[0])

    f.close()
    return time

def extract_velocity_probability(filename, outfilename):
    time = (2/3) * compute_max_time(filename)
    velocity_modules = []

    current_time = 0

    f = open(filename, 'r')
    particle_index = 0
    count = 0
    has_count = False

    for line in f:
        data = line.rstrip("\n").split(" ")
        if len(data) == 1:
            current_time = float(data[0])
            particle_index = 0
            if count > 0:
                has_count = True
        if len(data) > 1:
            if particle_index > 0:
                if current_time > time:
                    x_velocity = float(data[2])
                    y_velocity = float(data[3])
                    velocity_modules.append((x_velocity**2 + y_velocity**2)**(1/2))
            particle_index += 1
            if not has_count:
                count += 1
    f.close()

    f = open(outfilename, 'a+')

    f.write(str(count))
    for v in velocity_modules:
        f.write(' {}'.format(v))
    f.write('\n')

    f.close()

def compute_velocity_probability(filename):
    time = (2/3) * compute_max_time(filename)
    velocity_modules = {}

    current_time = 0

    f = open(filename, 'r')
    particle_index = 0

    for line in f:
        data = line.rstrip("\n").split(" ")
        if not int(data[0]) in velocity_modules:
            velocity_modules[int(data[0])] = []
        vs = [float(x) for x in data[1:]]
        for v in vs:
            velocity_modules[int(data[0])].append(v)
    f.close()

    for k in velocity_modules:
        print("Data for {}".format(k))
        weights = np.ones_like(velocity_modules[k]) / len(velocity_modules[k])
        plt.hist(velocity_modules[k], bins=np.arange(min(velocity_modules[k]), max(velocity_modules[k]) + 0.25, 0.25), weights=weights)
        plt.gca().xaxis.set_minor_locator(MultipleLocator(0.25))
        plt.show()

def extract_velocity_probability_at_t0(filename, outfilename):
    f = open(filename, 'r')

    velocity_modules = []
    time = -1
    particle_index = 0
    count = 0
    has_count = False

    for line in f:
        data = line.rstrip("\n").split(" ")
        if len(data) == 1:
            if time >= 0:
                break
            time = float(data[0])
            particle_index = 0
            if count > 0:
                has_count = True
        if len(data) > 1:
            if particle_index > 0:
                x_velocity = float(data[2])
                y_velocity = float(data[3])
                velocity_modules.append((x_velocity**2 + y_velocity**2)**(1/2))
            particle_index += 1
            if not has_count:
                count += 1

    f.close()

    f = open(outfilename, 'a+')

    f.write(str(count))
    for v in velocity_modules:
        f.write(' {}'.format(v))
    f.write('\n')

    f.close()

def compute_velocity_probability_at_t0(filename):
    f = open(filename, 'r')

    velocity_modules = {}
    time = -1
    particle_index = 0

    for line in f:
        data = line.rstrip("\n").split(" ")
        if not int(data[0]) in velocity_modules:
            velocity_modules[int(data[0])] = []
        vs = [float(x) for x in data[1:]]
        for v in vs:
            velocity_modules[int(data[0])].append(v)

    f.close()

    for k in velocity_modules:
        print("Data for {}".format(k))
        weights = np.ones_like(velocity_modules[k]) / len(velocity_modules[k])
        plt.hist(velocity_modules[k], bins=np.arange(min(velocity_modules[k]), max(velocity_modules[k]) + 0.25, 0.25), weights=weights)
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
    plt.plot(points_x[0], points_y[0], 'go')
    plt.plot(points_x[-1], points_y[-1], 'ko')
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

    plt.plot(points_x, points_y, 'r', label = "Trayectoria con T1")
    # T2 -> Menor temp, T3 -> Mas temp
    plt.plot(points_x_slower, points_y_slower, 'g', label = "Trayectoria con T2")
    plt.plot(points_x_faster, points_y_faster, 'b', label = "Trayectoria con T3")
    plt.plot(points_x[0], points_y[0], 'kx')
    plt.plot(points_x[-1], points_y[-1], 'kx')
    plt.plot(points_x_slower[-1], points_y_slower[-1], 'kx')
    plt.plot(points_x_faster[-1], points_y_faster[-1], 'kx')
    plt.legend()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().xaxis.set_minor_locator(MultipleLocator(0.1))
    plt.gca().yaxis.set_minor_locator(MultipleLocator(0.1))
    plt.gca().set_xlabel('Posición X')
    plt.gca().set_ylabel('Posición Y')
    plt.xlim(radius, area_length - radius)
    plt.ylim(radius, area_length - radius)
    plt.savefig(IMAGES + 'Item_4/multiple_trajectory.png')


def generate_msd_frames(filename, clock_time, start_time, end_time, radius, L):
    f = open(filename, 'r')

    processed_iterations = {}
    processed_times = []
    skip = True
    index = 0
    particles_hit_wall = set([])
    delta = 0.001

    for line in f:
        data = line.rstrip("\n").split(" ")
        if len(data) == 1:
            index = 0
            time = float(data[0])
            if time > end_time:
                skip = True
            elif time >= start_time:
                processed_iterations[time] = []
                processed_times.append(time)
                skip = False
        else:
            if not skip:
                point = [float(x) for x in data]
                if abs(point[0] + radius[index] - L) < delta or abs(point[1] + radius[index] - L) < delta or abs(point[0] - radius[index]) < delta or abs(point[1] - radius[index]) < delta:
                    particles_hit_wall.add(index)
                processed_iterations[time].append(point)
                index += 1

    f.close()

    chosen_times = []

    # Add the first one
    chosen_times.append(processed_iterations[processed_times[0]])

    clock_current = start_time + clock_time

    for t in processed_times:
        if t >= clock_current:
            chosen_times.append(processed_iterations[t])
            clock_current += clock_time
            #if clock_current > 50:
            #    break

    return chosen_times, particles_hit_wall

def parse_static_file(filename):
    f = open(filename, 'r')

    radius = []
    index = 0
    length = 0

    for line in f:
        data = line.rstrip("\n").split(" ")
        if index > 0:
            radius.append(float(data[1]))
        else:
            length = float(data[0])
        index += 1

    return radius, length, index-1


def retrieve_particle_close_to_center(filename, radius, L, N, invalid_particles):
    # Want any particle within a unit length away from the center
    # Big particle has a radius of 0.7 and small on of 0.9 --> 0.1 length of range
    f = open(filename, 'r')
    min_dist = 100
    min_index = 0
    min_x_center = L/2
    min_y_center = L/2

    for line in f:
        data = line.rstrip("\n").split(" ")
        if len(data) == 1:
            time = float(data[0])
            index = 0
        # dont want to include the big particle
        elif len(data) > 1 and time <= 0:
            x = float(data[0]) - L/2
            y = float(data[1]) - L/2
            dist = (x**2 + y**2)**(1/2)
            if dist < min_dist and radius[index] < 0.5 and index not in invalid_particles:
                min_dist = dist
                min_index = index
                min_x_center = float(data[0])
                min_y_center = float(data[1])

            index += 1
        else:
            break

    return min_index, min_x_center, min_y_center


def compute_msd_for_run(input_filename, output_filename, type, radius, L, N):
    total_time = compute_max_time(input_filename)

    # Only want to consider the simulations with time longer than 50 seconds
    if total_time < 50:
        print('Total time (' + str(total_time) + ') must be larger than 50')
        return

    start_time = 25.0
    clock_time = start_time/10.0
    chosen_frames, particles_hit_wall = generate_msd_frames(input_filename, clock_time, start_time, 2*start_time, radius, L)

    if type == 'S':
        particle_index, x_center, y_center = retrieve_particle_close_to_center('./parsable_files/dynamic.txt', radius, L, N, particles_hit_wall)
        if particle_index == 0:
            print('No small particle that hasnt impacted with the wall')
            return
    else:
        particle_index, x_center, y_center = 0, L/2, L/2

    msd_stats = []
    for frame in chosen_frames:
        particle = frame[particle_index]

        x_displ = (particle[0] - x_center)**2
        y_displ = (particle[1] - y_center)**2
        msd_stats.append(x_displ + y_displ)

    output = open(output_filename, 'a')

    output.write('{}\t'.format(N))
    if particle_index == 0:
        output.write('B\t')
    else:
        output.write('S\t')

    for msd in msd_stats:
        output.write('{}\t'.format(msd))
    output.write('\n')

    output.close()


def calculate_msd_mean(msds):
    return statistics.mean(msds)

def calculate_msd_sd(msds, mean):
    if len(msds) > 1:
        return statistics.stdev(msds, mean)
    else:
        return 0


def organize_data(data):
    times = []
    means = []
    stds = []

    start_time = 25.0
    clock_time = start_time/10.0

    for msd in data:
        times = np.arange(start_time, 2*start_time, clock_time)
        means.append(msd['mean'])
        stds.append(msd['sd'])

    times, msds, sds = zip(*sorted(zip(times, means, stds)))
    return times, msds, sds

# Our approximation of the linear regression y = mx + b with b=0
def r(x, c):
    return c*x

# Calculate the mean and standard deviation of the MSD
def calculate_average_msd(filename):
    f = open(filename, 'r')
    stats = {}

    for line in f:
        data = line.rstrip("\t\n").split("\t")
        N = int(data[0])
        type = data[1]

        if not N in stats:
            stats[N] = {}

        if not type in stats[N]:
            stats[N][type] = []

        # Removing N and type fromt the data
        msds = [float(x) for x in data[2:]]

        index = 0
        for msd in msds:
            if len(stats[N][type]) <= index:
                stats[N][type].append([])
            stats[N][type][index].append(msd)
            index += 1

    for N in stats:
        for type in stats[N]:
            index = 0
            for msds in stats[N][type]:
                mean = calculate_msd_mean(msds)
                sd = calculate_msd_sd(msds, mean)
                stats[N][type][index] = {'mean': mean, 'sd': sd}
                index += 1

    for N in stats:
        for stat_type in stats[N]:
            plt.clf()

            f,(ax,ax2) = plt.subplots(1,2,sharey=True, facecolor='w', gridspec_kw={'width_ratios': [0.3, 7]})

            # Set the x axis label
            ax2.set_xlabel('Tiempo (s)')

            # Set the y axis label
            ax.set_ylabel('Desvio Cuadratico Medio')

            times, msds, sds = organize_data(stats[N][stat_type])

            ax2.scatter(times, msds)

            ax2.errorbar(times, msds, yerr=sds, fmt='o', color='black',
                             ecolor='lightgray', elinewidth=3, capsize=0)

            ax.scatter(times, msds)

            ax.errorbar(times, msds, yerr=sds, fmt='o', color='black',
                         ecolor='lightgray', elinewidth=3, capsize=0)

            min_error, c = calculate_regression(times, msds)

            ax.set_xlim(0,1)
            ax2.set_xlim(24,50)

            ax2.plot(times, [r(x,c) for x in times])
            ax.plot([0, 1], [r(x,c) for x in [0, 1]])

            # hide the spines between ax and ax2
            ax.spines['right'].set_visible(False)
            ax2.spines['left'].set_visible(False)
            ax2.yaxis.tick_right()

        # Make the spacing between the two axes a bit smaller
            plt.subplots_adjust(wspace=0.07)

            d = .015 # how big to make the diagonal lines in axes coordinates
            # arguments to pass plot, just so we don't keep repeating them
            kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
            ax.plot((1-d,1+d),(-d,+d), **kwargs) # top-left diagonal
            ax.plot((1-d,1+d),(1-d,1+d), **kwargs) # bottom-left diagonal

            kwargs.update(transform=ax2.transAxes) # switch to the bottom axes
            ax2.plot((-d,d),(-d,+d), **kwargs) # top-right diagonal
            ax2.plot((-d,d),(1-d,1+d), **kwargs) # bottom-right diagonal

            plt.savefig('images/' + str(N) + '_' + str(stat_type) + '_msd.png')


def calculate_regression(x_array, y_array):
    min_error = 100
    min_c = 100

    for c in np.arange(-2, 2, 0.001):
        error = 0
        for index in range(0, len(x_array)):
            error += (y_array[index] - r(x_array[index], c))**2

        if error < min_error:
            min_error = error
            min_c = c

    return min_error, min_c

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
    elif args.process_type == COLLISION_FREQUENCY_MEDIAN:
         print("Computing collision frquency median...")
         compute_collision_frequency_median('./parsable_files/collision_frequency.txt')
    elif args.process_type == EXTRACT_COLLISION_PROBABILITY:
        print("Extracting collision probability...")
        extract_collision_probability('./parsable_files/dynamic.txt', './parsable_files/collision_spans.txt')
    elif args.process_type == COMPUTE_COLLISION_PROBABILITY:
        print("Computing collision probability...")
        compute_collision_probability('./parsable_files/collision_spans.txt')
    elif args.process_type == TRAJECTORY_ONE:
        print("Computing trajectory...")
        compute_trajectory_one('./parsable_files/dynamic.txt', './parsable_files/static.txt')
    elif args.process_type == TRAJECTORY_MULTIPLE:
        print("Computing trajectory...")
        compute_trajectory_multiple('./parsable_files/dynamic.txt', './parsable_files/dynamic_slower.txt',  './parsable_files/dynamic_faster.txt', './parsable_files/static.txt')
    elif args.process_type == COMPUTE_VELOCITY_PROBABILITY:
        print("Computing velocity probability...")
        compute_velocity_probability('./parsable_files/velocity_probability.txt')
    elif args.process_type == EXTRACT_VELOCITY_PROBABILITY:
        print("Extracting velocity probability...")
        extract_velocity_probability('./parsable_files/dynamic.txt', './parsable_files/velocity_probability.txt')
    elif args.process_type == EXTRACT_VELOCITY_PROBABILITY_T0:
        print("Extracting velocity probability...")
        extract_velocity_probability_at_t0('./parsable_files/dynamic.txt', './parsable_files/velocity_probability_t0.txt')
    elif args.process_type == COMPUTE_VELOCITY_PROBABILITY_T0:
        print("Computing velocity probability...")
        compute_velocity_probability_at_t0('./parsable_files/velocity_probability_t0.txt')
    elif args.process_type == MSD_B:
        print("Computing MSD of main particle...")
        radius, L, N = parse_static_file('./parsable_files/static.txt')
        compute_msd_for_run('./parsable_files/dynamic.txt', './parsable_files/msd_stats.txt', 'B', radius, L, N)
    elif args.process_type == MSD_S:
        print("Computing MSD of small particle...")
        radius, L, N = parse_static_file('./parsable_files/static.txt')
        compute_msd_for_run('./parsable_files/dynamic.txt', './parsable_files/msd_stats.txt', 'S', radius, L, N)
    elif args.process_type == MSD_GRAPH:
        print("Creating MSD graph...")
        calculate_average_msd('./parsable_files/msd_stats.txt')

# call main
if __name__ == '__main__':
    main()

