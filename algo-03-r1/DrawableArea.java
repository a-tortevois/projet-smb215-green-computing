class DrawableArea implements Comparable<DrawableArea> {
    public int x;
    public int y;
    public int d;
    public int w;

    public DrawableArea(int x, int y, int d, int w) {
        this.x = x;
        this.y = y;
        this.d = d;
        this.w = w;
    }

    @Override
    public int compareTo(DrawableArea area) {
        if (this.d == area.d) {
            if (this.y == area.y) {
                return this.x - area.x;
            }
            return this.y - area.y;
        }
        return area.d - this.d;
    }
}