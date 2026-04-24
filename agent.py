LANE_WIDTH = None
LANES_X = None

class Agent:
    def __init__(self, lanes_x, lane_width, height):
        global LANE_WIDTH, LANES_X
        LANE_WIDTH = lane_width
        LANES_X = lanes_x
        self.x = LANES_X[1]
        self.y = height - 100
        self.speed = 10

    def calculate_utility(self, lane_x, obstacles):
        danger = 0
        for ob in obstacles:
            ox, oy = ob[0], ob[1]
            if abs(ox - lane_x) < LANE_WIDTH // 2 + 10:
                dist_y = self.y - oy
                if dist_y > 0:
                    danger += (100000 / (dist_y + 1))
        return 1000 - danger

    def think(self, obstacles):
        utilities = [self.calculate_utility(lx, obstacles) for lx in LANES_X]
        return LANES_X[utilities.index(max(utilities))]
