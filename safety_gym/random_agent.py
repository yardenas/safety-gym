#!/usr/bin/env python

from collections import defaultdict
import argparse

import gym
import numpy as np  # noqa

import safety_gym  # noqa


class ActionRepeat(gym.Wrapper):
  def __init__(self, env, repeat, sum_cost=False):
    assert repeat >= 1, 'Expects at least one repeat.'
    super(ActionRepeat, self).__init__(env)
    self.repeat = repeat
    self.sum_cost = sum_cost

  def step(self, action):
    done = False
    total_reward = 0.0
    current_step = 0
    total_cost = 0.0
    while current_step < self.repeat and not done:
      obs, reward, done, info = self.env.step(action)
      if self.sum_cost:
        total_cost += info['cost']
      total_reward += reward
      current_step += 1
    if self.sum_cost:
      info['cost'] = total_cost  # noqa
    return obs, total_reward, done, info  # noqa


def run_random(env_name):
  env = gym.make(env_name)
  env = ActionRepeat(env, 2, True)
  env.seed(0)
  obs = env.reset()
  done = False
  ep_ret = 0
  ep_cost = 0
  episodes = 0
  episode_actions = []
  data = []
  while episodes < 500:
    if done:
      episodes += 1
      print('Episode Return: %.3f \t Episode Cost: %.3f' % (ep_ret, ep_cost),
            "episodes {}".format(episodes))
      ep_ret, ep_cost = 0, 0
      data.append(np.array(episode_actions))
      episode_actions = []
      obs = env.reset()
    env.controller()
    act = env.controller.action.copy()
    episode_actions.append(act)
    obs, reward, done, info = env.step(act)
    ep_ret += reward
    ep_cost += info.get('cost', 0)
    img = env.render()
  np.savez_compressed('actions_repeat2.npz', actions=np.asarray(data))


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--env', default='Safexp-PointGoal2-v0')
  args = parser.parse_args()
  run_random(args.env)
