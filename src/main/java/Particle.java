public class Particle implements Comparable<Particle> {
    //////////////////////////////////////////////////////////////////////////////////////////
    //                                        PROPERTIES
    //////////////////////////////////////////////////////////////////////////////////////////

    // Convention, ID starts at 0
    private int id;
    private double x;
    private double y;
    private double vx;
    private double vy;
    private double radius;
    private double mass;

    //////////////////////////////////////////////////////////////////////////////////////////
    //                                        CONSTRUCTORS
    //////////////////////////////////////////////////////////////////////////////////////////

    public Particle(int id, double x, double y, double vx, double vy, double radius, double mass) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.radius = radius;
        this.mass = mass;
    }

    public Particle(int id, double radius, double mass) {
        this.id = id;
        this.radius = radius;
        this.mass = mass;
    }

    //////////////////////////////////////////////////////////////////////////////////////////
    //                                        GETTERS
    //////////////////////////////////////////////////////////////////////////////////////////

    public int getId() {
        return id;
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public double getVx() {
        return vx;
    }

    public double getVy() {
        return vy;
    }

    public double getRadius() {
        return radius;
    }

    public double getMass() {
        return mass;
    }

    //////////////////////////////////////////////////////////////////////////////////////////
    //                                        SETTERS
    //////////////////////////////////////////////////////////////////////////////////////////

    public void setX(double x) {
        this.x = x;
    }

    public void setY(double y) {
        this.y = y;
    }

    public void setVx(double vx) {
        this.vx = vx;
    }

    public void setVy(double vy) {
        this.vy = vy;
    }

    //////////////////////////////////////////////////////////////////////////////////////////
    //                                        METHODS
    //////////////////////////////////////////////////////////////////////////////////////////

    @Override
    public int hashCode() {
        return id;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || this.getClass() != o.getClass()) return false;
        Particle particle = (Particle) o;
        return this.id == particle.getId();
    }

    @Override
    public String toString() {
        return String.format("[Particle #%d] {x = %f, y = %f, radius = %f, mass = %f}\n",
                this.id,
                this.x,
                this.y,
                this.radius,
                this.mass
        );
    }

    public int compareTo(Particle particle) {
        return Integer.compare(id, particle.getId());
    }

    /**
     * Updates the particle's position according to a delta time
     * @param delta time to be used to update position
     */
    public void updatePositionForDelta(double delta){
        this.x = this.x + this.vx * delta;
        this.y = this.y + this.vy * delta;
    }

    /**
     * Calculates the time to collision with another particle
     * @param p other particle to take in consideration
     * @return delta of time to collision
     */
    public double calculateCollisionDelta(Particle p){
        // Calculating deltaV and deltaR
        double dvx = p.getVx() - this.vx;
        double dvy = p.getVy() - this.vy;
        double dx = p.getX() - this.x;
        double dy = p.getY() - this.y;

        double sigma = this.radius + p.getRadius();

        // Calculating dot product
        double dotdvdr = dvx * dx + dvy * dy;
        double dotdvdv = dvx * dvx + dvy * dvy;
        double dotdrdr = dx * dx + dy * dy;

        // Calculating d
        double d = Math.pow(dotdvdr, 2) - dotdvdv * (dotdrdr - Math.pow(sigma, 2));

        // Dot product between deltaV and delta R
        if (dotdvdr >= 0) {
            return Double.MAX_VALUE;
        } else if (d < 0) {
            return Double.MAX_VALUE;
        }
        return - ((dotdvdr + Math.sqrt(d)) / dotdvdv);
    }


    /**
     * Calculates the collision time to a wall, indicated by the index
     * @param wallIndex index of a wall (Constant.TOP_WALL_INDEX: top, -2: right, -3: bottom, Constant.LEFT_WALL_INDEX: left)
     * @param areaLength length of the area of study
     * @return delta of time to collision, max value if not possible
     */
    public double calculateCollisionDelta(int wallIndex, double areaLength){
        switch (wallIndex){
            case Constant.TOP_WALL_INDEX:
                return this.vy <= 0 ? Double.MAX_VALUE : (areaLength - this.radius - this.y)/this.vy;
            case Constant.RIGHT_WALL_INDEX:
                return this.vx <= 0 ? Double.MAX_VALUE : (areaLength - this.radius - this.x)/this.vx;
            case Constant.BOTTOM_WALL_INDEX:
                return this.vy >= 0 ? Double.MAX_VALUE : (this.radius - this.y)/this.vy;
            case Constant.LEFT_WALL_INDEX:
                return this.vx >= 0 ? Double.MAX_VALUE : (this.radius - this.x)/this.vx;
            default:
                return Double.MAX_VALUE;
        }
    }

    /**
     * Calculate the new velocity of a particle when colliding with a wall
     * @param wallIndex index of a wall (Constant.TOP_WALL_INDEX: top, Constant.RIGHT_WALL_INDEX: right, Constant.BOTTOM_WALL_INDEX: bottom, Constant.LEFT_WALL_INDEX: left)
     */
    public void calculateWallCollisionVelocity(int wallIndex) {
        if (wallIndex == Constant.TOP_WALL_INDEX || wallIndex == Constant.BOTTOM_WALL_INDEX) {
            // Hitting horizontal walls inverts the vy velocity
            this.vy = -1 * this.vy;
        } else {
            // Hitting vertical walls inverts the vx velocity
            this.vx = -1 * this.vx;
        }
    }

    public void calculateParticleCollisionVelocity(Particle p) {
        // Calculating deltaV and deltaR
        double dvx = p.getVx() - this.vx;
        double dvy = p.getVy() - this.vy;
        double dx = p.getX() - this.x;
        double dy = p.getY() - this.y;

        double sigma = this.radius + p.getRadius();

        // Calculating dot product
        double dotdvdr = dvx * dx + dvy * dy;
        // Calculate impulse conservation (Jx, Jy)
        double J = (2 * this.mass * p.getMass() * dotdvdr) / (sigma * (this.mass + p.getMass()));
        double Jx = (J * dx) / sigma;
        double Jy = (J * dy) / sigma;

        // Updating this particle's velocity
        this.vx = this.vx + (Jx / this.mass);
        this.vy = this.vy + (Jy / this.mass);
        // Updating other particles velocity
        p.setVx(p.getVx() - (Jx / p.getMass()));
        p.setVy(p.getVy() - (Jy / p.getMass()));
    }
}
