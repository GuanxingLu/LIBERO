#!/usr/bin/env python3

"""
This example demonstrates how to enable and use dense rewards in Libero.
"""

import numpy as np
import argparse
import os

from libero.libero import get_env_from_task
from libero.libero.benchmark import get_task

def get_libero_dummy_action():
    """Get dummy/no-op action, used to roll out the simulation while the robot does nothing."""
    return [0, 0, 0, 0, 0, 0, -1]

def main(args):
    # Get the task information
    task = get_task(args.benchmark, args.task_id)
    print(f"Task: {task.name}")
    print(f"Language instruction: {task.language}")
    
    # Create the environment with dense rewards enabled
    env = get_env_from_task(
        task=task.name,
        task_id=args.task_id,
        benchmark=args.benchmark,
        control_freq=args.control_freq,
        reward_shaping=True,  # Enable dense rewards
        # reward_shaping=False,
    )
    
    # Reset the environment
    obs = env.reset()
    
    # Run a random policy to demonstrate dense rewards
    rewards = []
    for i in range(args.steps):
        # Random action
        action = get_libero_dummy_action()
        
        # Step the environment
        obs, reward, done, info = env.step(action)
        rewards.append(reward)
        
        print(f"Step {i}, Reward: {reward:.4f}")
        
        # Break if the task is completed
        if done:
            print("Task completed!")
            break
    
    # Plot the reward curve if matplotlib is available
    # try:
    #     import matplotlib.pyplot as plt
    #     plt.figure(figsize=(10, 5))
    #     plt.plot(rewards)
    #     plt.title("Dense Rewards Over Time")
    #     plt.xlabel("Steps")
    #     plt.ylabel("Reward")
    #     plt.savefig("dense_reward_plot.png")
    #     print("Reward plot saved as dense_reward_plot.png")
    # except ImportError:
    #     print("Matplotlib not available for plotting.")
    
    env.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", type=str, default="libero_goal")
    # parser.add_argument("--benchmark", type=str, default="libero_10")
    parser.add_argument("--task_id", type=int, default=0)
    parser.add_argument("--control_freq", type=int, default=20)
    parser.add_argument("--steps", type=int, default=500)
    args = parser.parse_args()
    
    main(args) 