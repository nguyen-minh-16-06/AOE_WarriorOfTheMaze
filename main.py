import pygame
import sys
import time
import os
import csv
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.environment import MazeEnv
from src.asset_manager import AssetManager
from src.renderer import AnimatedRenderer
from src.q_learning import QLearningAgent


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AOE - WarriorOfTheMaze")
    clock = pygame.time.Clock()

    print(">>> ĐANG LOAD GAME!")

    # ====== INIT ======
    assets = AssetManager()
    env = MazeEnv()
    env.reset()
    renderer = AnimatedRenderer(env, assets)

    # --- INITIALIZE AGENT ---
    agent = QLearningAgent(epsilon = 0.5)

    if os.path.exists("q_table.pkl"):
        agent.load_model("q_table.pkl")
    else:
        print("Warning: q_table.pkl not found. Agent will run with empty brain.")

    # ====== VARIABLES ======
    episode_steps = []
    goal_times = []

    goal_start_time = None
    start_time = None
    total_time = None

    auto_run = False
    episode_count = 1
    step_count = 0
    running = True

    run_count = 0

    # Result Board State
    mission_completed = False
    final_total_time = 0
    final_total_steps = 0

    # Text mapping for console logs
    ORDINAL_MAP = {1: "nhất", 2: "hai", 3: "ba", 4: "tư", 5: "năm"}
    TOTAL_GOALS = len(env.initial_goals)

    # Output Dir
    os.makedirs("results", exist_ok = True)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(">>> QUIT GAME!")
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print(">>> QUIT GAME!")
                    running = False

                if event.key == pygame.K_SPACE:
                    if auto_run:
                        auto_run = False
                        print(">>> NHÀ VUA TRỞ VỀ 👑!")

                        env.agent_pos = env.start_pos
                        env.visited = [env.start_pos]
                        renderer.set_target(env.start_pos[0], env.start_pos[1])

                    else:
                        # --- BẮT ĐẦU CHẠY ---
                        auto_run = True
                        run_count += 1

                        if run_count == 1:
                            print(">>> BẮT ĐẦU NHIỆM VỤ!")
                        else:
                            print(">>> TIẾP TỤC ĐI SÁT PHẠT!")

                        env.reset()
                        episode_steps.clear()
                        goal_times.clear()
                        step_count = 0

                        start_time = time.time()
                        goal_start_time = start_time
                        total_time = None
                        mission_completed = False

                if event.key == pygame.K_s:
                    agent.save_model()
                    print(">>> ĐÃ LƯU Q-TABLE!")

                if event.key == pygame.K_r:
                    print(">>> RESET GAME!")
                    env.reset()
                    episode_count = 1
                    step_count = 0
                    run_count = 0
                    auto_run = False
                    episode_steps.clear()
                    goal_times.clear()
                    mission_completed = False

                    st = renderer.to_iso(9, 0)
                    renderer.curr_x, renderer.curr_y = st
                    renderer.target_x, renderer.target_y = st

        is_moving = renderer.update()

        # ====== AI LOGIC ======
        if auto_run and not is_moving:
            if not env.goals:
                auto_run = False
            else:
                # Target Hint
                current_goal_pos = env.goals[0]
                target_id = env.goal_ids[current_goal_pos]

                state = (env.agent_pos[0], env.agent_pos[1], target_id)

                action = agent.choose_action(state)

                # Step
                next_pos, reward, done = env.step(action)
                step_count += 1
                renderer.set_target(next_pos[0], next_pos[1])

                if done:
                    # Log Console
                    goals_destroyed = TOTAL_GOALS - len(env.goals)
                    ordinal_str = ORDINAL_MAP.get(goals_destroyed, str(goals_destroyed))
                    print(f">>> Mục tiêu thứ {ordinal_str} đã bị tiêu diệt!")

                    # Log Time
                    goal_elapsed = time.time() - goal_start_time
                    goal_times.append(goal_elapsed)
                    goal_start_time = time.time()

                    episode_steps.append(step_count)

                    # Reset Position
                    env.agent_pos = env.start_pos
                    st = renderer.to_iso(9, 0)
                    renderer.curr_x, renderer.curr_y = st
                    renderer.target_x, renderer.target_y = st

                    time.sleep(0.2)

                    episode_count += 1
                    step_count = 0

                if not env.goals:
                    total_time = time.time() - start_time
                    auto_run = False
                    env.visited = [env.start_pos]

                    print(">>> TẤT CẢ MỤC TIÊU ĐÃ BỊ TIÊU DIỆT!")

                    renderer.draw(screen)
                    renderer.draw_ui(screen, episode_count, step_count, 0, len(env.walls_created), total_time)
                    pygame.display.flip()

                    time.sleep(0.5)

                    print(">>> MISSION COMPLETED!")

                    # Activate Board
                    mission_completed = True
                    final_total_time = total_time
                    final_total_steps = sum(episode_steps)

                    os.makedirs("results/test", exist_ok = True)
                    with open("results/test/run_log.csv", "w", newline = "") as f:
                        writer = csv.writer(f)
                        writer.writerow(["goal_index", "time_sec"])
                        for i, t in enumerate(goal_times):
                            writer.writerow([i + 1, t])

                    plt.figure()
                    plt.plot(goal_times, marker = 'o')
                    plt.xlabel("Mục tiêu")
                    plt.ylabel("Thời gian (s)")
                    plt.title("Thời gian tìm ra mục tiêu trong 1 Episode")
                    plt.grid(True)
                    plt.savefig("results/test/Thời gian tìm ra mục tiêu của 1 Episode.png")
                    plt.close()

                    plt.figure()
                    plt.plot(episode_steps)
                    plt.xlabel("Episode")
                    plt.ylabel("Bước")
                    plt.title("Số bước trong một Episode")
                    plt.grid(True)
                    plt.savefig("results/test/Số bước trong một Episode.png")
                    plt.close()

        # ====== RENDER ======
        renderer.draw(screen)

        elapsed = 0
        if start_time and auto_run:
            elapsed = time.time() - start_time
        elif total_time:
            elapsed = total_time

        # Draw UI left of PyGame
        renderer.draw_ui(screen, episode_count, step_count, len(env.goals), len(env.walls_created), elapsed)

        # Draw table Mission Completed
        if mission_completed:
            start_episode_idx = episode_count - len(goal_times)

            renderer.draw_mission_board(screen, goal_times, episode_steps, final_total_time, final_total_steps, start_episode_idx)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()