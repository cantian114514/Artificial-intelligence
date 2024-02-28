### MDP Value Iteration and Policy Iteration
import argparse
import numpy as np
import gym
import time
from lake_envs import *

np.set_printoptions(precision=3)

parser = argparse.ArgumentParser(description='A program to run assignment 1 implementations.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--env", 
					help="The name of the environment to run your algorithm on.", 
					choices=["Deterministic-4x4-FrozenLake-v0","Stochastic-4x4-FrozenLake-v0"],
					default="Deterministic-4x4-FrozenLake-v0")

"""
For policy_evaluation, policy_improvement, policy_iteration and value_iteration,
the parameters P, nS, nA, gamma are defined as follows:

	P: nested dictionary
		From gym.core.Environment
		For each pair of states in [1, nS] and actions in [1, nA], P[state][action] is a
		tuple of the form (probability, nextstate, reward, terminal) where
			- probability: float
				the probability of transitioning from "state" to "nextstate" with "action"
			- nextstate: int
				denotes the state we transition to (in range [0, nS - 1])
			- reward: int
				either 0 or 1, the reward for transitioning from "state" to
				"nextstate" with "action"
			- terminal: bool
			  True when "nextstate" is a terminal state (hole or goal), False otherwise
	nS: int
		number of states in the environment
	nA: int
		number of actions in the environment
	gamma: float
		Discount factor. Number in range [0, 1)
"""

def policy_evaluation(P, nS, nA, policy, gamma=0.9, tol=1e-3): # 策略评估
	"""
	Evaluate the value function from a given policy.
	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	policy: np.array[nS]
		The policy to evaluate. Maps states to actions.
	tol: float
		Terminate policy evaluation when
			max |value_function(s) - prev_value_function(s)| < tol
	Returns
	-------
	value_function: np.ndarray[nS]
		The value function of the given policy, where value_function[s] is
		the value of state s
	"""
	value_function = np.zeros(nS)
	# start implement here
	while True:
		delta=0 # 记录总值看收敛情况
		for state in range(nS): # 遍历状态
			v=value_function[state] #保存当前状态的值函数
			q_values=np.zeros(nA) #计算每个动作的值函数
			for action in range(nA): #遍历动作
				for prob, next_state, reward, _ in P[state][action]:
					q_values[action]+=prob*(reward+gamma*value_function[next_state]) #update
			value_function[state]=np.max(q_values) #选出最大值
			delta=max(delta, np.abs(v-value_function[state]))
		if delta<tol: #小于阈值则认为收敛
			break
	return value_function


def policy_improvement(P, nS, nA, value_from_policy, policy, gamma=0.9): #策略提升
	"""Given the value function from policy improve the policy.
	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	value_from_policy: np.ndarray
		The value calculated from the policy
	policy: np.array
		The previous policy.
	Returns
	-------
	new_policy: np.ndarray[nS]
		An array of integers. Each integer is the optimal action to take
		in that state according to the environment dynamics and the
		given value function.
	"""
	new_policy = np.zeros(nS, dtype='int')
	# start implement here
	for state in range(nS):
		q_values=np.zeros(nA) # 算Q值
		for action in range(nA):
			for prob, next_state, reward, _ in P[state][action]:
				q_values[action]+=prob*(reward+gamma*value_from_policy[next_state])# update
		new_policy[state]=np.argmax(q_values) #选出Q值最大的策略
	return new_policy


def policy_iteration(P, nS, nA, gamma=0.9, tol=10e-3): # 策略迭代
	"""
	Runs policy iteration.
	You should call the policy_evaluation() and policy_improvement() methods to
	implement this method.
	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	tol: float
		tol parameter used in policy_evaluation()
	Returns:
	----------
	value_function: np.ndarray[nS]
	policy: np.ndarray[nS]
	"""
	value_function = np.zeros(nS)
	policy = np.zeros(nS, dtype=int)
	# start implement here
	while True:
		value_function=policy_evaluation(P, nS, nA, policy, gamma, tol)
		new_policy = policy_improvement(P, nS, nA, value_function, gamma)
		if np.array_equal(policy, new_policy): #如果策略不再改变，说明达到最优策略
			break
		policy = new_policy
	return value_function, policy

def value_iteration(P, nS, nA, gamma=0.9, tol=1e-3): #值迭代
	"""
	Learn value function and policy by using value iteration method for a given
	gamma and environment.
	Parameters:
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	tol: float
		Terminate value iteration when
			max |value_function(s) - prev_value_function(s)| < tol
	Returns:
	----------
	value_function: np.ndarray[nS]
	policy: np.ndarray[nS]
	"""
	value_function = np.zeros(nS)
	policy = np.zeros(nS, dtype=int)
	# start implement here
	while True:
		delta=0 #记录变化，来判断收敛情况
		for state in range(nS): # 遍历状态
			v=value_function[state] #保存当前状态的值函数
			q_values=np.zeros(nA) #动作的值函数
			for action in range(nA):
				for prob, next_state, reward, _ in P[state][action]:
					q_values[action]+=prob*(reward+gamma*value_function[next_state])
			value_function[state]=np.max(q_values) #取最大的Q值 然后更新
			delta=max(delta, np.abs(v-value_function[state]))
		if delta<tol: #判断收敛
			break

	for state in range(nS):
		q_values = np.zeros(nA)
		for action in range(nA):
			for prob, next_state, reward, _ in P[state][action]:
				q_values[action]+=prob*(reward+gamma*value_function[next_state])
		policy[state] = np.argmax(q_values)
	return value_function, policy

def render_single(env, policy, max_steps=100):
	"""
	This function does not need to be modified
	Renders policy once on environment. Watch your agent play!

	Parameters
	----------
	env: gym.core.Environment
		Environment to play on. Must have nS, nA, and P as attributes.
	Policy: np.array of shape [env.nS]
		The action to take at a given state
	"""
	episode_reward = 0
	ob = env.reset()
	done = False
	for t in range(max_steps):
		env.render()
		time.sleep(0.25)
		a = policy[ob]
		ob, rew, done, _ = env.step(a)
		episode_reward += rew
		if done:
			break
	env.render()
	if not done:
		print("The agent didn't reach a terminal state in {} steps.".format(max_steps))
	else:
		print("Episode reward: %f" % episode_reward)


# Edit below to run policy and value iteration on different environments and
# visualize the resulting policies in action!
# You may change the parameters in the functions below
if __name__ == "__main__":
	# read in script argument
	args = parser.parse_args()
	
	# Make gym environment
	env = gym.make(args.env)

	print("\n" + "-"*25 + "\nBeginning Policy Iteration\n" + "-"*25)

	V_pi, p_pi = policy_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-3)
	render_single(env, p_pi, 100)

	print("\n" + "-"*25 + "\nBeginning Value Iteration\n" + "-"*25)

	V_vi, p_vi = value_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-3)
	render_single(env, p_vi, 100)