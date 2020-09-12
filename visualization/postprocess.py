from numpy import random
import math
import argparse
import random as rnd

# Usage examples
# python3 generator/input_generator.py -L 6 -N 101 -r 0.2 -m 0.9 -R 0.7 -M 2 -v 2 -retry 40

def generate_animation_frames(filename, clock_time):
    f = open(filename, 'r')

    processed_iterations = {}
    processed_times = []

    for line in f:
        data = line.rstrip("\n").split(" ")
        if len(data) == 1:
            time = float(data[0])
            processed_iterations[time] = []
            processed_times.append(time)
        else:
            point = [float(x) for x in data]
            processed_iterations[time].append(point)

    chosen_times = []

    # Add the first one
    chosen_times.append(processed_iterations[processed_times[0]])

    clock_current = clock_time

    for t in processed_times:
        if t >= clock_current:
            chosen_times.append(processed_iterations[t])
            clock_current += clock_time

    return chosen_times

def parse_particle_radius(filename):
    f = open(filename, 'r')

    radius = []
    index = 0
    length = 0

    for line in f:
        data = line.rstrip("\n").split(" ")
        if index > 0:
            radius.append(data[1])
        else:
            length = float(data[0])
        index += 1

    return radius, length

def generate_animation_file(filename, chosen_frames, particle_radius, area_length):
    f = open(filename, 'w')
    n = len(particle_radius)

    for frames in chosen_frames:
        f.write('{}\n'.format(n + 4))
        f.write('\n')
        point_index = 0

        # Adding the particles
        for points in frames:
            f.write('{}\t{}\t{}\n'.format(particle_radius[point_index], points[0], points[1]))
            point_index += 1

        # Adding dummy particles
        f.write('{}\t{}\t{}\n'.format(0.00001, area_length, area_length))
        f.write('{}\t{}\t{}\n'.format(0.00001, 0, area_length))
        f.write('{}\t{}\t{}\n'.format(0.00001, area_length, 0))
        f.write('{}\t{}\t{}\n'.format(0.00001, 0, 0))

    f.close()

# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Post processing for the points data to generate animation frames")

    # add arguments
    parser.add_argument('-t', dest='clock_time', required=True)
    args = parser.parse_args()

    # Parsing the radius
    particle_radius, area_length = parse_particle_radius('./parsable_files/static.txt')

    # Generating the points
    chosen_frames = generate_animation_frames('./parsable_files/dynamic.txt', float(args.clock_time))

    generate_animation_file('./parsable_files/animation.xyz', chosen_frames, particle_radius, area_length)

# call main
if __name__ == '__main__':
    main()

