import glfw

import numpy as np


class Controller:
  def __init__(self, mode='point'):
    self.action = np.zeros((2,))
    self._mode = mode

  def reset(self):
    self.action = np.zeros_like(self.action)

  def __call__(self):
    assert glfw.joystick_present(glfw.JOYSTICK_1)
    cmd = glfw.get_joystick_axes(glfw.JOYSTICK_1)[0]
    y = -cmd[1] if np.abs(cmd[1]) > 0.05 else 0.0
    x = -cmd[0] if np.abs(cmd[0]) > 0.05 else 0.0
    self.action[0] = np.clip(y, -0.03, 1.0)
    self.action[1] = x

