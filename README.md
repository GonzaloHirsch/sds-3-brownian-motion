# Simulación de Sistemas - TP3

## File Generation
File generation is done randomnly, without superposition.

To run the file generation:
```
python3 generator/input_generator.py -L 6 -N 101 -r 0.2 -m 0.9 -R 0.7 -M 2 -v 2 -retry 40
```

Where:
 - **L** -> Area length
 - **N** -> Amount of particles, without counting the big one (100 < N < 150)
 - **r** -> Radius of small particles
 - **m** -> Mass of small particles
 - **R** -> Radius of big particle
 - **M** -> Mass of big particle
 - **v** -> Max velocity module
 - **retry** -> Amount of retries in case of not finding spot for particle (the bigger the better, but take into account the time it takes)