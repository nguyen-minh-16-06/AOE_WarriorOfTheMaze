from src.environment import MazeEnv
from src.q_learning import QLearningAgent
import csv
import os
import matplotlib.pyplot as plt
import numpy as np

def train():
    os.makedirs("results/training", exist_ok = True)

    # ===== INIT =====
    env = MazeEnv()
    agent = QLearningAgent(epsilon = 1.0, learning_rate = 0.1, discount_factor = 0.99)

    # ===== PARAMETERS =====
    EPISODES = 10000
    MAX_STEPS = 400
    EPSILON_MIN = 0.01
    EPSILON_DECAY = 0.9995

    # ===== LOGGING =====
    log_file = open("results/training/training_log.csv", "w", newline = "")
    writer = csv.writer(log_file)
    writer.writerow(["episode", "steps", "reward", "epsilon"])

    episode_steps = []
    episode_rewards = []
    episode_epsilons = []

    for episode in range(1, EPISODES + 1):
        env.reset()
        total_reward = 0
        total_steps = 0

        while env.goals and total_steps < MAX_STEPS * 5:
            visited_positions = set()
            visited_positions.add(env.agent_pos)

            current_goal_pos = env.goals[0]
            target_id = env.goal_ids[current_goal_pos]

            state = (env.agent_pos[0], env.agent_pos[1], target_id)

            steps = 0
            while steps < MAX_STEPS:
                action = agent.choose_action(state)
                next_pos, reward, done = env.step(action)

                if next_pos in visited_positions:
                    reward -= 10
                else:
                    reward += 1
                    visited_positions.add(next_pos)

                next_target_id = target_id

                if done:
                    visited_positions.clear()
                    visited_positions.add(env.start_pos)

                    if env.goals:
                        next_goal_pos = env.goals[0]
                        next_target_id = env.goal_ids[next_goal_pos]
                    else:
                        next_target_id = -1

                next_state = (next_pos[0], next_pos[1], next_target_id)

                agent.learn(state, action, reward, next_state)

                state = next_state
                total_reward += reward
                steps += 1
                total_steps += 1

                if done:
                    env.agent_pos = env.start_pos
                    break

            if steps >= MAX_STEPS:
                break

        # ===== RECORD DATA =====
        episode_steps.append(total_steps)
        episode_rewards.append(total_reward)
        episode_epsilons.append(agent.epsilon)
        writer.writerow([episode, total_steps, total_reward, agent.epsilon])

        if agent.epsilon > EPSILON_MIN:
            agent.epsilon *= EPSILON_DECAY

        if episode % 100 == 0:
            print(f"Episode {episode} | Steps: {total_steps} | Reward: {total_reward:.2f} | Epsilon: {agent.epsilon:.3f}")

    log_file.close()
    agent.save_model("q_table.pkl")

    # ===== PLOT RESULT =====
    plt.figure()
    plt.plot(episode_epsilons)
    plt.xlabel("Episode")
    plt.ylabel("Epsilon")
    plt.title("Số Epsilon trong một Eposide")
    plt.grid(True)
    plt.savefig("results/training/Số Epsilon trong một Eposide.png")
    plt.close()

    plt.figure()
    plt.plot(episode_steps)
    plt.xlabel("Episode")
    plt.ylabel("Bước")
    plt.title("Số bước trong một Episode")
    plt.grid(True)
    plt.savefig("results/training/Số bước trong một Episode.png")
    plt.close()

    avg_rewards = []
    for i in range(0, len(episode_rewards), 100):
        avg_rewards.append(np.mean(episode_rewards[i:i + 100]))

    plt.figure()
    plt.plot(avg_rewards)
    plt.xlabel("Episode")
    plt.ylabel("Phần thưởng")
    plt.title("Phần thưởng trung bình")
    plt.grid(True)
    plt.savefig("results/training/Phần thưởng trung bình.png")
    plt.close()

    print("ĐÃ HUẤN LUYỆN XONG MÔ HÌNH")

if __name__ == "__main__":
    train()