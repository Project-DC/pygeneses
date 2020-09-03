import unittest
import numpy as np
import os
import shutil

from pygeneses.envs.prima_vita.player_class import Player
from pygeneses.envs.prima_vita import PrimaVita


class TestPlayerClass(unittest.TestCase):
    def test_initial_x_y(self):
        player = Player(i=1, log_dir=".", tob=10, energy=200, x=100, y=300)
        self.assertEqual(player.action_history, [[100, 300]])

    def test_add_parent_single_parent(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200)
        player.add_parent(id=1, tob=0)
        self.assertEqual(player.action_history[1][0], 1)
        self.assertEqual(player.action_history[1][1], 0)

    def test_add_parent_two_parents(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200)
        player.add_parent(id=1, tob=0, mate_id=2, mate_tob=3)
        self.assertEqual(player.action_history[1][0][0], 1)
        self.assertEqual(player.action_history[1][0][1], 0)
        self.assertEqual(player.action_history[1][1][0], 2)
        self.assertEqual(player.action_history[1][1][1], 3)

    def test_write_data(self):
        model = PrimaVita(log_dir_info="test")
        if not os.path.exists(model.log_dir):
            os.mkdir(model.log_dir)

        player = Player(i=1, log_dir=model.log_dir, tob=10, energy=200)
        player.write_data(time=10, alive_count=10)

        self.assertTrue(os.path.exists(os.path.join(model.log_dir, "10-1.npy")))

        shutil.rmtree(model.log_dir)

    def test_update_history_action_less_equal_9(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.states.append([-1, -1])
        player.update_history(action=7, time=10, reward=-2)

        check_vals = [7, 10, -2, 200, 0, 0, [-1, -1]]

        for i in range(len(check_vals)):
            with self.subTest("Check action history for an action <= 9", i=i):
                self.assertEqual(player.action_history[-1][i], check_vals[i])

    def test_update_history_action_asexual_reproduction(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.states.append([-1, -1])
        player.update_history(
            action=10, time=10, reward=-2, num_offspring=2, offspring_ids=[11, 12]
        )

        check_vals = [10, 10, -2, 200, 2, [11, 12], 0, 0, [-1, -1]]

        for i in range(len(check_vals)):
            if i != 5:
                with self.subTest("Check action history for failed action", i=i):
                    self.assertEqual(player.action_history[-1][i], check_vals[i])
            else:
                with self.subTest("Check action history for failed action", i=i):
                    self.assertEqual(player.action_history[-1][i][0], check_vals[i][0])
                    self.assertEqual(player.action_history[-1][i][1], check_vals[i][1])

    def test_update_history_action_sexual_reproduction(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.states.append([-1, -1])
        player.update_history(
            action=11,
            time=10,
            reward=-2,
            num_offspring=2,
            offspring_ids=[11, 12],
            mate_id=5,
        )

        check_vals = [11, 10, -2, 200, 2, [11, 12], 5, 0, 0, [-1, -1]]

        for i in range(len(check_vals)):
            if i != 5:
                with self.subTest("Check action history for failed action", i=i):
                    self.assertEqual(player.action_history[-1][i], check_vals[i])
            else:
                with self.subTest("Check action history for failed action", i=i):
                    self.assertEqual(player.action_history[-1][i][0], check_vals[i][0])
                    self.assertEqual(player.action_history[-1][i][1], check_vals[i][1])

    def test_update_history_action_fight(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.states.append([-1, -1])
        player.update_history(action=12, time=10, reward=-2, fight_with=6)

        check_vals = [12, 10, -2, 200, 6, 0, 0, [-1, -1]]

        for i in range(len(check_vals)):
            with self.subTest("Check action history for failed action", i=i):
                self.assertEqual(player.action_history[-1][i], check_vals[i])

    def test_change_x_position(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.change_player_xposition(3)

        self.assertEqual(player.playerX, 3)
        self.assertEqual(player.energy, 198)

    def test_change_x_position_cannot_move(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.cannot_move = True
        player.change_player_xposition(3)

        self.assertEqual(player.playerX, 0)
        self.assertEqual(player.energy, 200)

    def test_change_x_position_negative_x(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.change_player_xposition(-3)

        self.assertEqual(player.playerX, 0)
        self.assertEqual(player.energy, 198)

    def test_change_x_position_out_of_screen(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200, x=1164, y=0)
        player.change_player_xposition(5)

        self.assertEqual(player.playerX, 1168)
        self.assertEqual(player.energy, 198)

    def test_change_y_position(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.change_player_yposition(3)

        self.assertEqual(player.playerY, 3)
        self.assertEqual(player.energy, 198)

    def test_change_y_position_cannot_move(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.cannot_move = True
        player.change_player_yposition(3)

        self.assertEqual(player.playerY, 0)
        self.assertEqual(player.energy, 200)

    def test_change_y_position_negative_x(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.change_player_yposition(-3)

        self.assertEqual(player.playerX, 0)
        self.assertEqual(player.energy, 198)

    def test_change_y_position_out_of_screen(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=664)
        player.change_player_yposition(5)

        self.assertEqual(player.playerY, 668)
        self.assertEqual(player.energy, 198)

    def test_change_y_position_no_energy_change(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.change_player_yposition(3, no_energy_change=True)

        self.assertEqual(player.playerY, 3)
        self.assertEqual(player.energy, 200)

    def test_asexual_reproduction(self):
        player = Player(i=2, log_dir=".", tob=10, energy=200, x=0, y=0)
        len_players = 10
        offspring_players, offspring_ids = player.asexual_reproduction(
            len_players=len_players, time_given=25, initial_energy=200
        )

        self.assertEqual(len(offspring_players), len(offspring_ids))

        for i in range(len(offspring_ids)):
            with self.subTest("Testing offspring ids in asexual reproduction", i=i):
                self.assertEqual(offspring_ids[i], len_players + i)
                self.assertEqual(offspring_players[i].action_history[-1][0], 2)
                self.assertEqual(offspring_players[i].action_history[-1][1], 10)

    def test_sexual_reproduction_gen_offspring(self):
        player = Player(i=2, log_dir=".", tob=10, energy=200, x=0, y=0)
        len_players = 10
        offspring_players, offspring_ids = player.sexual_reproduction(
            mating_begin_time=30,
            len_players=len_players,
            initial_energy=200,
            gen_offspring=True,
            mate_id=3,
            mate_tob=12,
        )

        self.assertEqual(len(offspring_players), len(offspring_ids))

        self.assertEqual(player.energy, 170)
        self.assertEqual(player.cannot_move, True)
        self.assertEqual(player.mating_begin_time, 30)

        for i in range(len(offspring_ids)):
            with self.subTest("Testing offspring ids in asexual reproduction", i=i):
                self.assertEqual(offspring_ids[i], len_players + i)
                self.assertEqual(offspring_players[i].action_history[-1][0][0], 2)
                self.assertEqual(offspring_players[i].action_history[-1][0][1], 10)
                self.assertEqual(offspring_players[i].action_history[-1][1][0], 3)
                self.assertEqual(offspring_players[i].action_history[-1][1][1], 12)

    def test_sexual_reproduction_no_gen_offspring(self):
        player = Player(i=2, log_dir=".", tob=10, energy=200, x=0, y=0)
        len_players = 10
        player.sexual_reproduction(
            mating_begin_time=30,
            len_players=len_players,
            initial_energy=200,
            gen_offspring=False,
            mate_id=3,
            mate_tob=12,
        )

        self.assertEqual(player.energy, 170)
        self.assertEqual(player.cannot_move, True)
        self.assertEqual(player.mating_begin_time, 30)

    def test_ingesting_food(self):
        player = Player(i=2, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.ingesting_food(idx=50, time_given=45)

        self.assertEqual(player.energy, 300)
        self.assertEqual(player.cannot_move, True)
        self.assertEqual(player.ingesting_begin_time, 45)
        self.assertEqual(player.ingesting_particle_index, 50)
