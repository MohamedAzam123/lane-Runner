BASE_SPEED = 4

def reset_game(Agent, LANES_X, LANE_WIDTH, HEIGHT):
    player = Agent(LANES_X, LANE_WIDTH, HEIGHT)
    obstacles = []
    score = 0
    spawn_timer = 0
    return player, obstacles, score, spawn_timer