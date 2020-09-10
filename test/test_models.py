import unittest
import numpy as np
import torch
import torch.optim as optim

from pygeneses.models.reinforce.reinforce import ReinforceModel
from pygeneses.models.reinforce.reinforce_nn import Agent

class TestReinforceModelClass(unittest.TestCase):
    def test_initializer(self):
        model = ReinforceModel(initial_population=2, state_size=21, action_size=13)

        for i in range(2):
            with self.subTest("Check initializing agent arrays", i=i):
                self.assertTrue(isinstance(model.agents[i], Agent))
                self.assertTrue(isinstance(model.optimizers[i], optim.Adam))
                self.assertTrue(isinstance(model.saved_log_probs[i], list))
                self.assertTrue(isinstance(model.policy_loss[i], list))
                self.assertTrue(isinstance(model.rewards[i], list))

        self.assertEqual(len(model.agents), 2)
        self.assertEqual(len(model.optimizers), 2)
        self.assertEqual(len(model.scores), 2)
        self.assertEqual(len(model.saved_log_probs), 2)
        self.assertEqual(len(model.policy_loss), 2)
        self.assertEqual(len(model.rewards), 2)

    def test_predict_action(self):
        model = ReinforceModel(initial_population=2, state_size=21, action_size=13)

        model.predict_action(0, np.array([0] * 21))
        self.assertEqual(len(model.saved_log_probs[0]), 1)

    def test_update_reward(self):
        model = ReinforceModel(initial_population=2, state_size=21, action_size=13)

        model.update_reward(0, 2)
        self.assertEqual(len(model.rewards[0]), 1)
        self.assertEqual(model.rewards[0], [2])

    def test_add_agents(self):
        model = ReinforceModel(initial_population=2, state_size=21, action_size=13)

        model.add_agents(parent_idx=0, num_offsprings=5)

        for i in range(5):
            with self.subTest("Check adding agents", i=i):
                self.assertTrue(isinstance(model.agents[i+2], Agent))
                self.assertTrue(isinstance(model.optimizers[i+2], optim.Adam))
                self.assertTrue(isinstance(model.saved_log_probs[i+2], list))
                self.assertTrue(isinstance(model.policy_loss[i+2], list))
                self.assertTrue(isinstance(model.rewards[i+2], list))

        self.assertEqual(len(model.agents), 7)
        self.assertEqual(len(model.optimizers), 7)
        self.assertEqual(len(model.scores), 7)
        self.assertEqual(len(model.saved_log_probs), 7)
        self.assertEqual(len(model.policy_loss), 7)
        self.assertEqual(len(model.rewards), 7)

    def test_kill_agents(self):
        model = ReinforceModel(initial_population=2, state_size=21, action_size=13)

        idx = 0
        model.kill_agent(idx)

        self.assertEqual(model.agents[idx], 0)
        self.assertEqual(model.optimizers[idx], 0)
        self.assertEqual(model.scores[idx], 0)
        self.assertEqual(model.saved_log_probs[idx], 0)
        self.assertEqual(model.policy_loss[idx], [])
        self.assertEqual(model.rewards[idx], 0)

    def test_update_single_agent(self):
        model = ReinforceModel(initial_population=2, state_size=21, action_size=13)

        model.update_single_agent(0)

        self.assertTrue(isinstance(model.policy_loss[0], list))
