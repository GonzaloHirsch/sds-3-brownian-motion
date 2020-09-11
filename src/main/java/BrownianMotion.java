import com.sun.xml.internal.ws.wsdl.writer.document.Part;

import java.util.*;
import java.util.stream.Collectors;

public class BrownianMotion {
    private final Map<Integer, Particle> particles;
    private final double areaLength;

    private static final int TOP_WALL_INDEX = -1;
    private static final int RIGHT_WALL_INDEX = -2;
    private static final int BOTTOM_WALL_INDEX = -3;
    private static final int LEFT_WALL_INDEX = -4;
    private static final int[] WALLS = new int[]{TOP_WALL_INDEX, RIGHT_WALL_INDEX, BOTTOM_WALL_INDEX, LEFT_WALL_INDEX};

    public BrownianMotion(final double areaLength, final Map<Integer, Particle> particles){
        // Map all particles to the id
        this.particles = particles;
        this.areaLength = areaLength;
    }

    /**
     * Method that simulates an iteration of the algorithm, it calculates the first collision and then updates particles acording to the calculated time
     * @return Collection of Particles with the given particles
     */
    public Collection<Particle> simulateUntilCollision(){
        // Calculate particle-particle or particle-wall collision
        CollisionInformation information = this.computeCollisions();

        // Update the positions of all particles
        this.updateParticlePositionsForDelta(information.delta);

        // Update the velocity of the collided particles
        this.updateCollidedParticlesVelocity(information);

        return this.particles.values();
    }

    /**
     * Given a delta of time, updates the positions of all the particles based on the movement equations
     * @param delta of time to be used in order to update
     */
    private void updateParticlePositionsForDelta(double delta){
        // TODO: HACER ESTO
    }

    /**
     * Given collision information, updates the involved particles' velocity
     * @param information for the collision, as returned by the computing algorithm
     */
    private void updateCollidedParticlesVelocity(CollisionInformation information){
        // TODO: HACER ESTO
    }

    /**
     * Method to compute the collisions and determine the first collision to be updated.
     * <br><br>
     * The algorithm takes advantage of the particle IDs in order to compute only half of the comparisons.
     * <br><br>
     * How it works?
     * <br><br>
     * It starts comparing with particle 0 and compares with particles 1 to n. Then, it compares particle 1 with 2 to n.
     * <br>
     * Generalizing, for particle k, it compares only particles k + 1 to n, to avoid duplicate comparisons
     * @return CollisionInformation object with the information to be able to perform updates
     */
    private CollisionInformation computeCollisions(){
        // Minimum time to beat with the collisions
        double minimumTime = Integer.MAX_VALUE;

        /*
        IDs of the particles involved in collisions, convention is that if it is a wall, the second id is negative
        Convention for ids:
         - -1 -> top wall
         - -2 -> right wall
         - -3 -> bottom wall
         - -4 -> left wall
        */
        int firstParticleId = 0;
        int secondParticleId = 0;

        // Variables to use during iteration
        Particle current, other;
        double currentTime;

        for (int index = 0; index < this.particles.size(); index++){
            current = this.particles.get(index);

            // Compare to other particles
            for (int subIndex = index + 1; subIndex < this.particles.size(); subIndex++){
                // Get the particle
                other = this.particles.get(subIndex);

                // Calculate collision time
                currentTime = current.calculateCollisionDelta(other);

                // Update minimum time information
                if (currentTime < minimumTime){
                    minimumTime = currentTime;
                    firstParticleId = current.getId();
                    secondParticleId = other.getId();
                }
            }

            // Compare to the walls
            for (int wall : WALLS){
                currentTime = current.calculateCollisionDelta(wall, this.areaLength);
                if (currentTime < minimumTime){
                    minimumTime = currentTime;
                    firstParticleId = current.getId();
                    secondParticleId = wall;
                }
            }
        }

        // Generating the information object and returning it
        return new CollisionInformation(firstParticleId, secondParticleId, minimumTime);
    }

    /**
     * Class to wrap collision information that is needed after a collision calculation is performed
     */
    public static class CollisionInformation{
        private final int firstParticleId;
        private final int secondParticleId;
        private final double delta;

        public CollisionInformation(int firstParticleId, int secondParticleId, double delta) {
            this.firstParticleId = firstParticleId;
            this.secondParticleId = secondParticleId;
            this.delta = delta;
        }

        public int getFirstParticleId() {
            return firstParticleId;
        }

        public int getSecondParticleId() {
            return secondParticleId;
        }

        public double getDelta() {
            return delta;
        }
    }
}
