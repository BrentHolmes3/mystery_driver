import random
import numpy as np
import gym
from gym import spaces
import pandas as pd

class F1MysteryDriverEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self, df):
        super(F1MysteryDriverEnv, self).__init__()
        
        self.df = df
        self.action_space = spaces.Discrete(len(df['driver']))  # Drivers are unique
        self.observation_space = spaces.Dict({
            "attempts": spaces.Discrete(6),  # A max of 6 attempts
            "feedback": spaces.MultiDiscrete([3] * 6)  # Feedback for each hint category
        })
        self.reset()

    def reset(self):
        self.state = {
            "mystery_driver": random.choice(self.df['driver']),
            "attempts": 0,
        }
        self.state["mystery_driver_info"] = self.df.loc[
            self.df['driver'] == self.state["mystery_driver"],
            ['car_number', 'start year', 'birth year', 'flag', 'team', 'wins']
        ].values[0]
        
        initial_observation = {
            "attempts": self.state["attempts"],
            "feedback": np.zeros(6)  # Initial feedback is all zeros (no information)
        }
        return initial_observation

    def step(self, action):
        assert self.action_space.contains(action)
        entered_driver = self.df['driver'].iloc[action]  # Map action to the driver name
        reward = 0
        done = False
        info = {}
        
        # Initialize feedback with whatever default you find suitable, e.g., np.zeros(6)
        feedback = np.zeros(6)
        
        if entered_driver == self.state["mystery_driver"]:
            reward = 10  # For choosing the correct driver
            done = True
            info["message"] = f"Correct! It is {self.state['mystery_driver_info']} YOU WIN!"
        else:
            self.state["attempts"] += 1
            feedback = self.get_feedback(entered_driver)  # Generate feedback based on the driver
            if self.state["attempts"] < 6:
                reward = -1  # Negative reward for incorrect guess
            else:
                # The feedback calculation is already done above, so we can remove it from here
                reward = -10  # More substantial negative reward for losing the game
                done = True
                info["message"] = "Game Over. Reached maximum attempts."
        
        observation = {
            "attempts": self.state["attempts"],
            "feedback": feedback
        }

        return observation, reward, done, info
    
    def get_feedback(self, entered_driver):
        feedback = np.zeros(6)  # We have 6 pieces of feedback

        # Number comparison
        entered_driver_number = self.df.loc[self.df['driver'] == entered_driver, 'car_number'].values[0]
        if entered_driver_number > self.state["mystery_driver_info"][0]:
            feedback[0] = -1
        elif entered_driver_number < self.state["mystery_driver_info"][0]:
            feedback[0] = 1

        # Birth year comparison
        entered_driver_birth_year = self.df.loc[self.df['driver'] == entered_driver, 'birth year'].values[0]
        if entered_driver_birth_year > self.state["mystery_driver_info"][2]:
            feedback[1] = -1
        elif entered_driver_birth_year < self.state["mystery_driver_info"][2]:
            feedback[1] = 1

        # Start year comparison
        entered_driver_start_year = self.df.loc[self.df['driver'] == entered_driver, 'start year'].values[0]
        if entered_driver_start_year > self.state["mystery_driver_info"][1]:
            feedback[2] = -1
        elif entered_driver_start_year < self.state["mystery_driver_info"][1]:
            feedback[2] = 1

        # Wins comparison
        entered_driver_wins = self.df.loc[self.df['driver'] == entered_driver, 'wins'].values[0]
        if entered_driver_wins > self.state["mystery_driver_info"][5]:
            feedback[3] = -1
        elif entered_driver_wins < self.state["mystery_driver_info"][5]:
            feedback[3] = 1

        # Flag comparison
        entered_driver_flag = self.df.loc[self.df['driver'] == entered_driver, 'flag'].values[0]
        feedback[4] = 0 if entered_driver_flag == self.state["mystery_driver_info"][3] else 1

        # Team comparison 
        entered_driver_team = self.df.loc[self.df['driver'] == entered_driver, 'team'].values[0]
        if entered_driver_team == self.state["mystery_driver_info"][4]:
            feedback[5] = 0
        else:
            feedback[5] = 1
        return feedback
        
    def render(self, mode='human'):
        # You can print out game state, feedback, or any other user-friendly information
        print(f"Attempts: {self.state['attempts']}")

    def close(self):
        # Perform any cleanup, if necessary
        pass

# A simple Q-learning agent class
class QLearningAgent:
    def __init__(self, action_space, state_space, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0, max_exploration_rate=1.0, min_exploration_rate=0.01, exploration_decay_rate=0.001):
        self.action_space = action_space
        self.state_space = state_space
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.max_exploration_rate = max_exploration_rate
        self.min_exploration_rate = min_exploration_rate
        self.exploration_decay_rate = exploration_decay_rate
        self.q_table = np.zeros((state_space, action_space.n))

    # QLearningAgent class - inside the class definition
    def get_state_as_int(self, observation):
        # Since feedback can be -1, 0, 1, first map these values to 0, 1, 2 for non-negative encoding
        mapped_feedback = observation['feedback'] + 1  # Shift from [-1, 0, 1] to [0, 1, 2]
        base = 3  # Now we use base 3 because we have three possible values: 0, 1, 2
        
        feedback_int = 0
        for i, val in enumerate(mapped_feedback):
            feedback_int *= base
            feedback_int += val
        
        # Calculate the state by combining attempts and feedback values
        state_int = observation['attempts'] * (base ** len(mapped_feedback)) + feedback_int
        return state_int
        
    def choose_action(self, observation):
        state = self.get_state_as_int(observation)
        exploration_rate_threshold = np.random.uniform(0, 1)
        if exploration_rate_threshold > self.exploration_rate:
            action = np.argmax(self.q_table[state])  # Exploit the best known value
        else:
            action = self.action_space.sample()  # Explore action space
        return action

    def learn(self, state, action, reward, next_state, done):
        old_value = self.q_table[state, action]
        next_max = np.max(self.q_table[next_state])
        
        new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (reward + self.discount_factor * next_max)
        self.q_table[state, action] = new_value
        
        if done:
            self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_rate_decay)

# Load the driver data and initialize the environment
df = pd.read_excel('./driver_data_base.xlsx')
env = F1MysteryDriverEnv(df)

# The feedback vector length is assumed to be 6 based on the env setup
feedback_vector_length = 6
# Each feedback element has 3 possible values (after mapping the original values)
num_feedback_options = 3 ** feedback_vector_length

# Total number of attempts
num_attempts = env.observation_space.spaces['attempts'].n

# Calculate total state space size
total_state_space_size = num_attempts * num_feedback_options

# Initialize Q-learning agent
agent = QLearningAgent(env.action_space, total_state_space_size)

# Hyperparameters
number_of_episodes = 10

# Training loop
for episode in range(number_of_episodes):
    observation = env.reset()
    state = agent.get_state_as_int(observation)
    total_reward = 0
    done = False
    steps = 0
    
    while not done and steps < num_attempts:
        action = agent.choose_action(observation)
        next_observation, reward, done, info = env.step(action)
        next_state = agent.get_state_as_int(next_observation)
        agent.learn(state, action, reward, next_state, done)

        state = next_state
        observation = next_observation
        total_reward += reward
        steps += 1

    print(f"Episode {episode + 1} finished with total reward: {total_reward}")

    # Adjust the exploration rate
    agent.exploration_rate = max(agent.min_exploration_rate, agent.exploration_rate * np.exp(-agent.exploration_decay_rate*episode))

# Optionally, save your Q-table to a file
np.save('q_table.npy', agent.q_table) 
