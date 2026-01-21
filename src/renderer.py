import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_WIDTH, TILE_HEIGHT, MOVE_SPEED, ANIMATION_SPEED

class AnimatedRenderer:
    def __init__(self, env, assets):
        # ===== INIT =====
        self.env = env
        self.assets = assets
        self.start_x = SCREEN_WIDTH // 2
        self.start_y = (SCREEN_HEIGHT - (env.rows + env.cols) * TILE_HEIGHT // 2) // 2 + 50

        st = self.to_iso(env.start_pos[0], env.start_pos[1])
        self.curr_x, self.curr_y = st
        self.target_x, self.target_y = st
        self.is_moving = False

        # ===== FONTS & COLORS =====
        self.font_ui = pygame.font.SysFont('Arial', 18, bold = True)
        self.font_title = pygame.font.SysFont('Arial', 32, bold = True)
        self.font_stat = pygame.font.SysFont('Arial', 20, bold = True)

        self.COLOR_YELLOW = (255, 255, 0)
        self.COLOR_CYAN = (0, 255, 255)
        self.COLOR_WHITE = (255, 255, 255)

    # ===== CALCULATIONS =====
    def to_iso(self, r, c):
        x = (c - r) * (TILE_WIDTH // 2) + self.start_x
        y = (c + r) * (TILE_HEIGHT // 2) + self.start_y
        return x, y

    def set_target(self, r, c):
        tx, ty = self.to_iso(r, c)
        self.target_x, self.target_y = tx, ty
        if abs(tx - self.curr_x) > 1 or abs(ty - self.curr_y) > 1:
            self.is_moving = True

    def update(self):
        if not self.is_moving: return False

        dx = self.target_x - self.curr_x
        dy = self.target_y - self.curr_y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist < MOVE_SPEED:
            self.curr_x, self.curr_y = self.target_x, self.target_y
            self.is_moving = False
        else:
            self.curr_x += (dx / dist) * MOVE_SPEED
            self.curr_y += (dy / dist) * MOVE_SPEED
        return self.is_moving

    # ===== DRAW GAME WORLD =====
    def draw(self, screen):
        screen.fill((30, 35, 40))
        for r in range(self.env.rows):
            for c in range(self.env.cols):
                self._draw_cell(screen, r, c)
        self._draw_agent(screen)

    def _draw_cell(self, screen, r, c):
        x, y = self.to_iso(r, c)

        # Floor
        img = self.assets.get_image('floor', seed = r * c)
        if img: screen.blit(img, img.get_rect(center = (x, y + TILE_HEIGHT // 2)))

        # Footprint
        if (r, c) in self.env.visited:
            pygame.draw.circle(screen, (255, 255, 0, 50), (x, y + 16), 3)

        # Object
        obj = None
        off_y = 0

        if (r, c) == self.env.start_pos:
            obj = self.assets.get_image('start')
            off_y = 10
        elif (r, c) in self.env.goals:
            obj = self.assets.goal_image
            if obj: obj = pygame.transform.flip(obj, True, False)
            off_y = 15
        elif self.env.grid[r, c] == 1 or (r, c) in self.env.walls_created:
            obj = self.assets.get_image('wall', seed = r * 10 + c)
            off_y = 25

        if obj:
            draw_x = x - obj.get_width() // 2
            draw_y = (y + TILE_HEIGHT // 2) - obj.get_height() + 10 + off_y
            if (r, c) in self.env.goals:
                draw_y = (y + TILE_HEIGHT // 2) - obj.get_height() + 15
            screen.blit(obj, (draw_x, draw_y))

    def _draw_agent(self, screen):
        img = self.assets.agent_image
        if not img: return

        pygame.draw.ellipse(screen, (0, 0, 0), (self.curr_x - 12, self.curr_y + TILE_HEIGHT // 2 - 6, 24, 12))
        draw_x = self.curr_x - img.get_width() // 2
        draw_y = self.curr_y + TILE_HEIGHT // 2 - img.get_height() + 15
        screen.blit(img, (draw_x, draw_y))

    # ===== DRAW UI & HUD =====
    def draw_ui(self, screen, episode_count, step_count, goals_len, walls_len, elapsed_time):
        ui_bg = pygame.Surface((320, 70))
        ui_bg.set_alpha(150)
        ui_bg.fill((0, 0, 0))
        screen.blit(ui_bg, (5, 5))

        screen.blit(self.font_ui.render(f"Episode: {episode_count} | Steps: {step_count}", True, self.COLOR_YELLOW),
                    (15, 10))
        screen.blit(self.font_ui.render(f"Goals: {goals_len} | Walls: {walls_len}", True, self.COLOR_WHITE), (15, 35))
        screen.blit(self.font_ui.render(f"Time: {elapsed_time:.2f}s", True, self.COLOR_CYAN), (200, 10))

    def draw_mission_board(self, screen, goal_times, episode_steps, total_time, total_steps, start_episode):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        panel_w, panel_h = 560, 320
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = (SCREEN_HEIGHT - panel_h) // 2

        panel_surf = pygame.Surface((panel_w, panel_h))
        panel_surf.fill((0, 0, 0))
        panel_surf.set_alpha(100)
        screen.blit(panel_surf, (panel_x, panel_y))

        title_surf = self.font_title.render("MISSION COMPLETED!", True, self.COLOR_YELLOW)
        title_rect = title_surf.get_rect(center = (SCREEN_WIDTH // 2, panel_y + 40))
        screen.blit(title_surf, title_rect)

        start_y_list = panel_y + 80
        line_height = 30

        for i in range(len(goal_times)):
            s_step = episode_steps[i]
            s_time = goal_times[i]

            current_ep_num = start_episode + i

            txt_ep = self.font_stat.render(f"Episode {current_ep_num}", True, self.COLOR_YELLOW)
            txt_step = self.font_stat.render(f"Steps: {s_step}", True, self.COLOR_WHITE)
            txt_time = self.font_stat.render(f"Time: {s_time:.2f}s", True, self.COLOR_CYAN)

            row_y = start_y_list + i * line_height

            screen.blit(txt_ep, (panel_x + 40, row_y))
            screen.blit(txt_step, (panel_x + 200, row_y))
            screen.blit(txt_time, (panel_x + 400, row_y))

        pygame.draw.line(screen, (100, 100, 100), (panel_x + 20, start_y_list + 160),
                         (panel_x + panel_w - 20, start_y_list + 160), 1)

        sum_y = start_y_list + 180
        sum_steps_txt = self.font_stat.render(f"Total Steps: {total_steps}", True, self.COLOR_WHITE)
        screen.blit(sum_steps_txt, (panel_x + 40, sum_y))

        sum_time_txt = self.font_stat.render(f"Total Time: {total_time:.2f}s", True, self.COLOR_CYAN)
        screen.blit(sum_time_txt, (panel_x + 350, sum_y))