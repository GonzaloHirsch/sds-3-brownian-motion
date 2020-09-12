import com.sun.xml.internal.ws.wsdl.writer.document.Part;

import java.util.*;
import java.util.stream.Collectors;

public class BrownianMotion {
    private final Map<Integer, Particle> particles;
    private TreeSet<CollisionInformation> collisions = new TreeSet<>();
    private final double areaLength;

    private double elapsedTime = 0;
    private boolean mainHasHitWall = false;

    private static final int[] WALLS = new int[]{Constant.TOP_WALL_INDEX, Constant.RIGHT_WALL_INDEX, Constant.BOTTOM_WALL_INDEX, Constant.LEFT_WALL_INDEX};

    public BrownianMotion(final double areaLength, final Map<Integer, Particle> particles){
        // Map all particles to the id
        this.particles = particles;
        this.areaLength = areaLength;

        // Computing all the collisions one time
        this.computeStartingCollisions();
    }

    /**
     * Given a delta of time, updates the positions of all the particles based on the movement equations
     * and the updated times till the other collisions
     * @param delta of time to be used in order to update
     */
    private void updateParticlePositionsForDelta(double delta){
        this.particles.values().forEach(p -> p.updatePositionForDelta(delta));
    }

    /**
     * Given collision information, updates the involved particles' velocity
     * @param information for the collision, as returned by the computing algorithm
     */
    private void updateCollidedParticlesVelocity(CollisionInformation information){
        if (information.firstParticleId >= 0){

        }

        if (information.secondParticleId >= 0){
            
        }
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
    private void computeStartingCollisions(){
        Particle current, other;
        int n = this.particles.size();

        for (int index = 0; index < n; index++){
            current = this.particles.get(index);
            for (int sub_index = index + 1; sub_index < n; sub_index++){
                other = this.particles.get(sub_index);

                // Computing the collision
                collisions.add(new CollisionInformation(current.getId(), other.getId(), current.calculateCollisionDelta(other)));
            }

            // Compare to the walls
            for (int wall : WALLS){
                collisions.add(new CollisionInformation(current.getId(), wall, current.calculateCollisionDelta(wall, this.areaLength)));
            }
        }
    }

    /**
     * Method that simulates an iteration of the algorithm, it calculates the first collision and then updates particles acording to the calculated time
     * @return Collection of Particles with the given particles
     */
    public Collection<Particle> simulateUntilCollision() {
        // Get the first collision that's going to happen
        CollisionInformation currentCollision = this.collisions.first();

        // Check if the collision was for the main particle
        this.checkIfMainHitWall(currentCollision);

        // Remove the unwanted collisions
        this.collisions = this.collisions.stream().filter(c -> c.firstParticleId != currentCollision.firstParticleId && c.firstParticleId != currentCollision.secondParticleId && c.secondParticleId != currentCollision.firstParticleId && c.secondParticleId != currentCollision.secondParticleId).collect(Collectors.toCollection(TreeSet::new));

        // Updating the deltas for each remaining collision
        this.collisions.forEach(c -> c.delta -= currentCollision.delta);

        // Updating the particle positions for a given delta
        this.updateParticlePositionsForDelta(currentCollision.getDelta());

        // Updating the velocities for the collided particles
        this.updateCollidedParticlesVelocity(currentCollision);

        // Incrementing the elapsed time
        this.elapsedTime += currentCollision.getDelta();

        Particle current, other;
        int n = this.particles.size();

        // Check if it's not a wall
        if (currentCollision.firstParticleId >= 0){
            // Get the particle to have it's collisions recalculated
            current = this.particles.get(currentCollision.firstParticleId);

            // Calculate the new collisions
            for (int index = 0; index < n; index++){
                if (index != currentCollision.firstParticleId){
                    other = this.particles.get(index);
                    collisions.add(new CollisionInformation(current.getId(), other.getId(), current.calculateCollisionDelta(other)));
                }
            }

            // Compare to the walls
            for (int wall : WALLS){
                collisions.add(new CollisionInformation(current.getId(), wall, current.calculateCollisionDelta(wall, this.areaLength)));
            }
        }

        // Check if not a wall
        if (currentCollision.secondParticleId >= 0){
            // Get the particle to have it's collisions recalculated
            current = this.particles.get(currentCollision.secondParticleId);

            // Calculate the new collisions
            for (int index = 0; index < n; index++){
                if (index != currentCollision.secondParticleId && index != currentCollision.firstParticleId){
                    other = this.particles.get(index);
                    collisions.add(new CollisionInformation(current.getId(), other.getId(), current.calculateCollisionDelta(other)));
                }
            }

            // Compare to the walls
            for (int wall : WALLS){
                collisions.add(new CollisionInformation(current.getId(), wall, current.calculateCollisionDelta(wall, this.areaLength)));
            }
        }

        return this.particles.values();
    }

    /**
     * Check if given the CollisionInformation, the main particle has hit the wall
     * @param c Collision information
     */
    private void checkIfMainHitWall(CollisionInformation c){
        if (c.firstParticleId == 0 || c.secondParticleId == 0){
            if (c.firstParticleId < 0 || c.secondParticleId < 0){
                this.mainHasHitWall = true;
            }
        }
    }

    public double getElapsedTime() {
        return elapsedTime;
    }

    public boolean mainHasHitWall() {
        return mainHasHitWall;
    }

    /**
     * Class to wrap collision information that is needed after a collision calculation is performed
     */
    public static class CollisionInformation implements Comparable<CollisionInformation> {
        private final int firstParticleId;
        private final int secondParticleId;
        private double delta;

        public CollisionInformation(int firstParticleId, int secondParticleId, double delta) {
            this.firstParticleId = Math.min(firstParticleId, secondParticleId);
            this.secondParticleId = Math.max(firstParticleId, secondParticleId);
            this.delta = delta;
        }

        public double getDelta() {
            return delta;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            CollisionInformation that = (CollisionInformation) o;
            return firstParticleId == that.firstParticleId &&
                    secondParticleId == that.secondParticleId;
        }

        @Override
        public int hashCode() {
            return Objects.hash(firstParticleId, secondParticleId);
        }

        @Override
        public int compareTo(CollisionInformation collision) {
            return Double.compare(this.delta, collision.delta);
        }
    }
}
