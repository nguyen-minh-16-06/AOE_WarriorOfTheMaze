import random
from src.config import MAZE_LAYOUT

class MazeEnv:
    def __init__(self):
        self.grid = MAZE_LAYOUT.copy()
        self.rows, self.cols = self.grid.shape
        self.start_pos = (9, 0)
        self.initial_goals = [(0, 0), (0, 4), (0, 9), (4, 9), (9, 9)]
        self.goal_ids = {pos: i for i, pos in enumerate(self.initial_goals)}

        self.goals = []
        self.walls_created = []
        self.agent_pos = self.start_pos
        self.visited = [self.start_pos]

    def reset(self):
        self.agent_pos = self.start_pos
        self.visited = [self.start_pos]
        self.walls_created = []

        self.goals = self.initial_goals.copy()
        random.shuffle(self.goals)

        return self.agent_pos

    def step(self, action):
        # 0: Up, 1: Down, 2: Left, 3: Right
        moves = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}
        dr, dc = moves[action]
        nr, nc = self.agent_pos[0] + dr, self.agent_pos[1] + dc

        if (nr < 0 or nr >= self.rows or nc < 0 or nc >= self.cols or
                self.grid[nr, nc] == 1 or (nr, nc) in self.walls_created):
            return self.agent_pos, -100, False

        self.agent_pos = (nr, nc)
        self.visited.append(self.agent_pos)

        reward = -1
        done = False

        if self.agent_pos in self.goals:
            self.goals.remove(self.agent_pos)
            self.walls_created.append(self.agent_pos)
            reward = 100
            done = True

        return self.agent_pos, reward, done