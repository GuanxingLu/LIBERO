# Dense Rewards in LIBERO

This document explains the dense reward implementation in LIBERO and how to use it in reinforcement learning algorithms.

## Introduction

LIBERO tasks originally used sparse rewards, where the agent only receives a reward of +1 when the task is completed. While this is conceptually simple, it makes learning difficult for reinforcement learning algorithms, especially for complex manipulation tasks.

The new dense reward implementation provides continuous feedback to the agent based on its progress toward task completion, making it easier for reinforcement learning algorithms to learn effective policies.

## How Dense Rewards Work

The dense reward system works by:

1. Evaluating progress toward each goal condition
2. Calculating distance-based metrics for common predicates (e.g., "on", "in")
3. Converting these distances into normalized progress values between 0 and 1
4. Using the minimum progress across all goal conditions as the overall reward

This implementation is particularly beneficial for multi-step tasks where the agent needs to satisfy multiple conditions.

## Supported Predicates

The dense reward implementation currently supports the following predicates:

- **Binary predicates**:
  - `on`: Provides rewards based on horizontal alignment between objects
  - `in`: Provides rewards based on 3D distance between objects

- **Unary predicates**:
  - `open`: Provides rewards based on how open an object is
  - `close`: Provides rewards based on how closed an object is

More predicates can be added by extending the `_get_predicate_progress` method in `BDDLBaseDomain`.

## Usage in RL Algorithms

### Enabling Dense Rewards

To enable dense rewards, set `reward_shaping=True` when creating the environment:

```python
env = get_env_from_task(
    task=task_name,
    reward_shaping=True,  # Enable dense rewards
    # ... other parameters
)
```

### Example with a Basic RL Algorithm

Here's a simple example using dense rewards with a basic RL algorithm:

```python
import gym
from stable_baselines3 import SAC
from libero.libero import get_env_from_task
from libero.libero.benchmark import get_task

# Get task info
task = get_task("libero_10", 0)

# Create environment with dense rewards
env = get_env_from_task(
    task=task.name,
    task_id=0,
    benchmark="libero_10",
    reward_shaping=True,  # Enable dense rewards
)

# Create RL agent
model = SAC("MlpPolicy", env, verbose=1)

# Train the agent
model.learn(total_timesteps=100000)

# Save the trained model
model.save("sac_libero_dense")

# Test the trained policy
obs = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()
```

## Benefits for RL

Dense rewards provide several benefits for reinforcement learning:

1. **Faster Learning**: By providing continuous feedback, the agent can learn much faster than with sparse rewards.
2. **Better Exploration**: The agent can follow the reward gradient to explore relevant parts of the state space.
3. **Stability**: Dense rewards provide more stable learning signals, reducing variance in policy updates.
4. **Task Decomposition**: Complex tasks are automatically broken down into simpler subgoals through the reward function.

## Limitations

While dense rewards are beneficial, they come with some limitations:

1. **Reward Design Complexity**: The reward function becomes more complex and might need tuning for different tasks.
2. **Potential for Reward Hacking**: Poorly designed dense rewards can lead to agents finding unintended shortcuts.
3. **Generalization**: Dense rewards might be less generalizable across different task variations than sparse rewards.

## Extending the Implementation

To extend the dense reward system to support additional predicates:

1. Open `libero/libero/envs/bddl_base_domain.py`
2. Find the `_get_predicate_progress` method
3. Add a new condition for your predicate, implementing an appropriate distance metric
4. Make sure your progress measure returns a value between 0 and 1 