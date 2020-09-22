public enum Walls {
    TOP_WALL_INDEX(-1),
    RIGHT_WALL_INDEX(-2),
    BOTTOM_WALL_INDEX(-3),
    LEFT_WALL_INDEX(-4);

    private int value;

    private Walls(int v){
        this.value = v;
    }

    public int getValue() {
        return value;
    }
}
