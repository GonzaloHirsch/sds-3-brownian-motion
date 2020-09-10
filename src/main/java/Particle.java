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
        // TODO: HACER ESTO
    }

    /**
     * Calculates the time to collision with another particle
     * @param p other particle to take in consideration
     * @return delta of time to collision
     */
    public double calculateCollisionDelta(Particle p){
        // TODO: HACER ESTO
        return 0;
    }

    /**
     * Calculates the collision time to a wall, indicated by the index
     * @param wallIndex index of a wall (-1: top, -2: right, -3: bottom, -4: left)
     * @param areaLength length of the area of study
     * @return delta of time to collision
     */
    public double calculateCollisionDelta(int wallIndex, double areaLength){
        // TODO: HACER ESTO
        return 0;
    }
}
