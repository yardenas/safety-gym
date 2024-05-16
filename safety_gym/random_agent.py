#!/usr/bin/env python

import argparse
import gym
import safety_gym  # noqa
import numpy as np  # noqa

import matplotlib.pyplot as plt

def run_random(env_name):
    env = gym.make(env_name)
    obs = env.reset()
    done = False
    ep_ret = 0
    ep_cost = 0
    while True:
        if done:
            print('Episode Return: %.3f \t Episode Cost: %.3f'%(ep_ret, ep_cost))
            ep_ret, ep_cost = 0, 0
            obs = env.reset()
        act = env.action_space.sample()
        obs, reward, done, info = env.step(act)
        ep_ret += reward
        ep_cost += info.get('cost', 0)
        img = env.render()
        plt.imshow(img)
        plt.pause(0.01)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--env', default='Safexp-DoggoGoal2-v0')
    args = parser.parse_args()
    run_random(args.env)
