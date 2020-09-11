# Simulación de Sistemas - TP3

## File Generation
File generation is done randomly, without superposition.

To run the file generation:
```
python3 generator/input_generator.py -L 6 -N 101 -r 0.2 -m 0.9 -R 0.7 -M 2 -v 2 -retry 100
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
 
## Ovito Configuration
A configuration is included in the repository inside _visualization/configuration.ovito_, it might have some issues with the loading. The Boundary Limits might need adjustments.

### Color Coding
In **Pipelines**(connection symbol), add a **Color Coding** modification.

Click the **Color Coding** modification added inside **Modifications**

Choose:
 - Operates On -> Particle
 - Input Property -> Mass
 - Color Gradient -> Blue-White-Red
 - End Value -> 2 (biggest mass)
 - Start Value -> 0.9 (smallest mass)
 
### Boundary Limits
In **Pipelines**(connection symbol), inside **Data Source**, click on **Simulation Cell**.

Choose:
 - Dimensionality -> 2D
 - Box Size Width -> 6
 - Box Size Length -> 6
 - Cell Origin -> [0, 0, 0]
 
### Particle Display
In **Pipelines**(connection symbol), inside **Visual Elements**, click on **Particles**.

Choose:
 - Shape -> Circle or Sphere (probably Circle gives better performance)

### File Format
The format for the files is **.XYZ**, this means it follows the given format:
```
Number of Particles
Timeframe (integer)
Mass1    Radius1    PositionX1  PositionY1   VelocityX1   VelocityY1
...
MassN    RadiusN    PositionXN  PositionYN   VelocityXN   VelocityYN
Number of Particles
Timeframe (integer)
Mass1    Radius1    PositionX1  PositionY1   VelocityX1   VelocityY1
...
MassN    RadiusN    PositionXN  PositionYN   VelocityXN   VelocityYN
Number of Particles
Timeframe (integer)
Mass1    Radius1    PositionX1  PositionY1   VelocityX1   VelocityY1
...
MassN    RadiusN    PositionXN  PositionYN   VelocityXN   VelocityYN
Number of Particles
Timeframe (integer)
Mass1    Radius1    PositionX1  PositionY1   VelocityX1   VelocityY1
...
MassN    RadiusN    PositionXN  PositionYN   VelocityXN   VelocityYN
...
```

Using this format for the file, the column mappings used are Mass, Radius, Position and Velocity respectively.