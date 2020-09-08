from numpy import random
import math
import argparse
import random as rnd

# Usage examples
# python3 generator/input_generator.py -L 6 -N 101 -r 0.2 -m 0.9 -R 0.7 -M 2 -v 2 -retry 40

# Returs a list of lists containing the points
# Each list has:
#  - 0 -> x coord
#  - 1 -> y coord
#  - 2 -> x velocity
#  - 3 -> y velocity
#  - 4 -> mass
#  - 5 -> radius
def generate_points(input_area_length, particle_number, small_radius, small_mass, big_radius, big_mass, velocity_mod_limit, retry_count):
    # List to hold all the points
    points = []

    # Adding the center particle
    points.append([input_area_length/2, input_area_length/2, 0, 0, big_mass, big_radius])

    points_added = 0
    tries = 0
    max_tries = retry_count

    while points_added < particle_number and tries < max_tries:
        # Generating coordinate
        target_x = random.uniform(0, input_area_length)
        target_y = random.uniform(0, input_area_length)

        # Radius and mass
        target_radius = small_radius
        target_mass = small_mass

        # Generating velocity, it is done using accepted answer in https://stackoverflow.com/questions/5837572/generate-a-random-point-within-a-circle-uniformly
        r = velocity_mod_limit * math.sqrt(random.uniform(0, 1))
        theta = random.uniform(0, 1) * 2 * math.pi
        target_vx = r * math.cos(theta)
        target_vy = r * math.sin(theta)

        # Verify it does not overlap others
        points_verified = 0
        while points_verified < len(points):
            point_prime = points[points_verified]
            distance = math.sqrt(((target_x - point_prime[0])**2) + ((target_y - point_prime[1])**2)) - target_radius - point_prime[5]
            if distance <= 0:
                break
            else:
                points_verified += 1

        # In this case it is ok
        if points_verified == len(points):
            points.append([target_x, target_y, target_vx, target_vy, target_mass, target_radius])
            points_added += 1
            tries = 0
        else:
            tries += 1

    # In this case it was not able to add more points
    if len(points) != particle_number + 1 and tries == max_tries:
        print("Could not add all required points, returning still")
        print("Could only generate", len(points), "out of", particle_number + 1 ,"points")
    else:
        print("Generated all points successfully")
    return points

# Generates the static file configuration given:
#   - filename -> Name of the static file to be used
#   - area_length -> Total length of the area of study
#   - points -> Points using the structure indicated at the top of the file
def generate_static_file(filename, area_length, points):
    f = open(filename, 'w')

    # Adding the amount of dimensions
    f.write('{}\n'.format(area_length))

    for point in points:
        f.write('{} {}\n'.format(point[4], point[5]))

    f.close()

# Generates the dynamic file configuration given:
#   - filename -> Name of the dynamic file to be used
#   - points -> Points using the structure indicated at the top of the file
def generate_dynamic_file(filename, points):
    f = open(filename, 'w')

    # We provide only the dynamic configuration at time 0
    f.write('0\n')

    # Adding the randomly generated
    for point in points:
        f.write('{} {} {} {}\n'.format(point[0], point[1], point[2], point[3]))

    f.close()

# Generates both the dynamic and the static file
def generate_files(area_length, points):
    generate_static_file('./parsable_files/static.txt', area_length, points)
    generate_dynamic_file('./parsable_files/dynamic.txt', points)

# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Generates random input for Brownian Motion")

    # add arguments
    parser.add_argument('-L', dest='area_length', required=True)
    parser.add_argument('-N', dest='particle_number', required=True)
    parser.add_argument('-r', dest='small_radius', required=True)
    parser.add_argument('-m', dest='small_mass', required=True)
    parser.add_argument('-R', dest='big_radius', required=True)
    parser.add_argument('-M', dest='big_mass', required=True)
    parser.add_argument('-v', dest='velocity_mod_limit', required=True)
    parser.add_argument('-retry', dest='retry_count', required=True)
    args = parser.parse_args()

    # Validations
    if int(args.particle_number) <= 100 or int(args.particle_number) >= 150:
        raise Exception("Particle number, must be 100 < N < 150")

    if float(args.small_radius) >= float(args.big_radius):
        raise Exception("Big radius must be bigger than small radius")

    if float(args.small_mass) >= float(args.big_mass):
        raise Exception("Big mass must be bigger than small mass")

    if float(args.velocity_mod_limit) <= 0:
        raise Exception("Velocity module must be > 0")

    # Generating the points
    points = generate_points(int(args.area_length), int(args.particle_number), float(args.small_radius), float(args.small_mass), float(args.big_radius), float(args.big_mass), float(args.velocity_mod_limit), int(args.retry_count))

    # Generating the files
    generate_files(int(args.area_length), points)

# call main
if __name__ == '__main__':
    main()

