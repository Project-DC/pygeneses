import unittest
import numpy as np
import os
import shutil

from pygeneses.envs.prima_vita.player_class import Player
from pygeneses.envs.prima_vita.particle_class import Particle
from pygeneses.envs.prima_vita import PrimaVita


class TestPlayerClass(unittest.TestCase):
    def test_initial_x_y(self):
        """
        Test initial x and y as passed in Player class' initializer
        """

        player = Player(i=1, log_dir=".", tob=10, energy=200, x=100, y=300)
        self.assertEqual(player.action_history, [[100, 300]])

    def test_add_parent_single_parent(self):
        """
        Test add_parent method in case of asexual reproduction (one parent)
        """

        player = Player(i=10, log_dir=".", tob=10, energy=200)
        player.add_parent(id=1, tob=0)
        self.assertEqual(player.action_history[1][0], 1)
        self.assertEqual(player.action_history[1][1], 0)

    def test_add_parent_two_parents(self):
        """
        Test add_parent method in case of sexual reproduction (two parents)
        """

        player = Player(i=10, log_dir=".", tob=10, energy=200)
        player.add_parent(id=1, tob=0, mate_id=2, mate_tob=3)
        self.assertEqual(player.action_history[1][0][0], 1)
        self.assertEqual(player.action_history[1][0][1], 0)
        self.assertEqual(player.action_history[1][1][0], 2)
        self.assertEqual(player.action_history[1][1][1], 3)

    def test_write_data(self):
        """
        Test write_data method which is used to write to log file once agent dies
        """

        model = PrimaVita(log_dir_info="test")
        if not os.path.exists(model.log_dir):
            os.mkdir(model.log_dir)

        player = Player(i=1, log_dir=model.log_dir, tob=10, energy=200)
        player.write_data(time=10, alive_count=10)

        self.assertTrue(os.path.exists(os.path.join(model.log_dir, "10-1.npy")))

        shutil.rmtree(model.log_dir)

    def test_update_history_action_less_equal_9(self):
        """
        Test update_history method for an action <= 9 (i.e. movement in 8 directions, stay, and ingestion),
        tested with action 7 here (moving south-east)
        """

        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.states.append([-1, -1])
        player.update_history(action=7, time=10, reward=-2)

        check_vals = [7, 10, -2, 200, 0, 0, [-1, -1]]

        for i in range(len(check_vals)):
            with self.subTest("Check action history for an action <= 9", i=i):
                self.assertEqual(player.action_history[-1][i], check_vals[i])

    def test_update_history_action_asexual_reproduction(self):
        """
        Test update_history method for action 10 (i.e. asexual reproduction)
        """

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
        """
        Test update_history method for action 11 (i.e. sexual reproduction)
        """

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
        """
        Test update_history method for action 12 (i.e. fight)
        """

        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.states.append([-1, -1])
        player.update_history(action=12, time=10, reward=-2, fight_with=6)

        check_vals = [12, 10, -2, 200, 6, 0, 0, [-1, -1]]

        for i in range(len(check_vals)):
            with self.subTest("Check action history for failed action", i=i):
                self.assertEqual(player.action_history[-1][i], check_vals[i])

    def test_change_x_position(self):
        """
        Test change_player_xposition (normal case)
        """

        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.change_player_xposition(3)

        self.assertEqual(player.playerX, 3)
        self.assertEqual(player.energy, 198)

    def test_change_x_position_cannot_move(self):
        """
        Test change_player_xposition (when agent is not allowed to move)
        """

        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.cannot_move = True
        player.change_player_xposition(3)

        self.assertEqual(player.playerX, 0)
        self.assertEqual(player.energy, 200)

    def test_change_x_position_negative_x(self):
        """
        Test change_player_xposition (edge case - when x becomes <= 0 i.e agent reaches left most side)
        """

        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.change_player_xposition(-3)

        self.assertEqual(player.playerX, 0)
        self.assertEqual(player.energy, 198)

    def test_change_x_position_out_of_screen(self):
        """
        Test change_player_xposition (edge case - when agent tries to go out of screen from right side)
        """

        player = Player(i=10, log_dir=".", tob=10, energy=200, x=1164, y=0)
        player.change_player_xposition(5)

        self.assertEqual(player.playerX, 1168)
        self.assertEqual(player.energy, 198)

    def test_change_y_position(self):
        """
        Test change_player_yposition (normal case)
        """

        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.change_player_yposition(3)

        self.assertEqual(player.playerY, 3)
        self.assertEqual(player.energy, 198)

    def test_change_y_position_cannot_move(self):
        """
        Test change_player_yposition (when agent is not allowed to move)
        """

        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.cannot_move = True
        player.change_player_yposition(3)

        self.assertEqual(player.playerY, 0)
        self.assertEqual(player.energy, 200)

    def test_change_y_position_negative_y(self):
        """
        Test change_player_yposition (edge case - when y becomes <= 0 i.e agent reaches top most side)
        """

        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.change_player_yposition(-3)

        self.assertEqual(player.playerX, 0)
        self.assertEqual(player.energy, 198)

    def test_change_y_position_out_of_screen(self):
        """
        Test change_player_yposition (edge case - when agent tries to go out of screen from bottom side)
        """

        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=664)
        player.change_player_yposition(5)

        self.assertEqual(player.playerY, 668)
        self.assertEqual(player.energy, 198)

    def test_change_y_position_no_energy_change(self):
        """
        Test change_player_xposition (when agent's energy is not supposed to decrease)
        """

        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.change_player_yposition(3, no_energy_change=True)

        self.assertEqual(player.playerY, 3)
        self.assertEqual(player.energy, 200)

    def test_asexual_reproduction(self):
        """
        Test asexual_reproduction
        """

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
        """
        Test sexual_reproduction for mother (i.e. gen_offspring = True)
        """

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
        """
        Test sexual_reproduction for father (i.e. gen_offspring = False)
        """

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
        """
        Test ingesting_food
        """

        player = Player(i=2, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.ingesting_food(idx=50, time_given=45)

        self.assertEqual(player.energy, 300)
        self.assertEqual(player.cannot_move, True)
        self.assertEqual(player.ingesting_begin_time, 45)
        self.assertEqual(player.ingesting_particle_index, 50)

class TestPrimaVitaClass(unittest.TestCase):
    def test_initializer(self):
        model = PrimaVita(log_dir_info="test")

        self.assertTrue(os.path.exists("Players_Data_test"))
        self.assertTrue(os.path.exists("Players_Data_test/Embeddings"))

        shutil.rmtree("Players_Data_test")

        # Testing init method (called from initialiazer)

        # Testing regenerate_species inside init method
        self.assertEqual(len(model.players), model.initial_population)

    def test_pad_state(self):
        model = PrimaVita(log_dir_info="test")

        # Greater than maxlen
        padded_state = model.pad_state([4, 3, 2, 1], 2)
        self.assertEqual(padded_state, [4, 3])

        # Less than maxlen
        padded_state = model.pad_state([4, 3], 4)
        self.assertEqual(list(padded_state), [4, 3, 0, 0])

        # Equal to maxlen
        padded_state = model.pad_state([4, 3, 2, 1], 4)
        self.assertEqual(padded_state, [4, 3, 2, 1])

        shutil.rmtree("Players_Data_test")

    def test_get_current_state(self):
        model = PrimaVita(log_dir_info="test", params_dic={"initial_population": 2})

        # Test state shape
        state, _ = model.get_current_state()
        self.assertEqual(state.shape, (2, 21))

        # Test stopping condition
        model.killed = [0, 1, 2]
        model.players = [0, 1, 2]

        _, running = model.get_current_state()

        self.assertEqual(running, False)

        shutil.rmtree("Players_Data_test")

    def test_update_time(self):
        model = PrimaVita(log_dir_info="test")

        model.update_time()
        self.assertEqual(model.time, 0)

        shutil.rmtree("Players_Data_test")

    def test_food_nearby(self):
        model = PrimaVita(log_dir_info="test", params_dic={"initial_population": 1})

        # Test dead player
        model.players = [1]
        food = model.food_nearby(model.players[0])

        self.assertEqual(food, -1)

        # Test food nearby
        model.players = [Player(i=0, log_dir="Players_Data_test", tob=10, x=50, y=500, energy=200)]
        model.food_particles = [Particle(x=64, y=514), Particle(x=45, y=502)]

        food = model.food_nearby(model.players[0])
        self.assertEqual(food, 0)

        shutil.rmtree("Players_Data_test")

    def test_food_in_env_no_get_idx(self):
        model = PrimaVita(log_dir_info="test", params_dic={"initial_population": 1})

        # Test dead player
        model.players = [1]
        food_env = model.food_in_env(model.players[0])

        self.assertEqual(food_env, -1)

        # Test food nearby
        model.players = [Player(i=0, log_dir="Players_Data_test", tob=10, x=50, y=500, energy=200)]
        model.food_particles = [Particle(x=64, y=514), Particle(x=45, y=502)]

        vec, distances = model.food_in_env(model.players[0])
        self.assertEqual(vec, [14, 14, -5, 2])
        self.assertEqual(distances, [19.79898987322333, 5.385164807134504])

        shutil.rmtree("Players_Data_test")

    def test_food_in_env_get_idx(self):
        model = PrimaVita(log_dir_info="test", params_dic={"initial_population": 1})

        # Test food nearby
        model.players = [Player(i=0, log_dir="Players_Data_test", tob=10, x=50, y=500, energy=200)]
        model.food_particles = [Particle(x=64, y=514), Particle(x=45, y=502)]

        vec, distances, env = model.food_in_env(model.players[0], get_idx=True)
        self.assertEqual(vec, [14, 14, -5, 2])
        self.assertEqual(distances, [19.79898987322333, 5.385164807134504])
        self.assertEqual(env, [0, 1])

        shutil.rmtree("Players_Data_test")

    def test_players_in_env_no_get_idx(self):
        model = PrimaVita(log_dir_info="test", params_dic={"initial_population": 1})

        # Test dead player
        model.players = [1]
        food_env = model.players_in_env(model.players[0])

        self.assertEqual(food_env, ([], []))

        # Test players nearby
        model.players = [Player(i=0, log_dir="Players_Data_test", tob=10, x=50, y=500, energy=200),
                         Player(i=1, log_dir="Players_Data_test", tob=12, x=48, y=505, energy=200)]

        vec, distances = model.players_in_env(model.players[0])
        self.assertTrue(vec[:-1], [2, -5])
        self.assertTrue(distances, [5.385164807134504])

        shutil.rmtree("Players_Data_test")

    def test_players_in_env_get_idx(self):
        model = PrimaVita(log_dir_info="test", params_dic={"initial_population": 2})

        # Test players nearby
        model.players = [Player(i=0, log_dir="Players_Data_test", tob=10, x=50, y=500, energy=200),
                         Player(i=1, log_dir="Players_Data_test", tob=12, x=48, y=505, energy=200)]

        vec, distances, env = model.players_in_env(model.players[0], get_idx=True)
        self.assertTrue(vec[:-1], [2, -5])
        self.assertTrue(distances, [5.385164807134504])
        self.assertTrue(env, [1])

        shutil.rmtree("Players_Data_test")

    def test_search_mate(self):
        model = PrimaVita(log_dir_info="test", params_dic={"initial_population": 3})

        # Test dead player
        model.players[0] = 1

        player = model.search_mate(model.players[0])
        self.assertEqual(player, -1)

        # Test find mate in radius
        model.players = [Player(i=0, log_dir="Players_Data_test", tob=10, x=50, y=500, energy=200),
                         Player(i=1, log_dir="Players_Data_test", tob=12, x=48, y=505, energy=200),
                         Player(i=2, log_dir="Players_Data_test", tob=12, x=40, y=530, energy=200)]

        model.players[0].is_impotent = False
        model.players[0].gender = "Male"

        model.players[1].is_impotent = False
        model.players[1].gender = "Female"

        model.time = 30

        player = model.search_mate(model.players[0])
        self.assertEqual(player, 1)

        shutil.rmtree("Players_Data_test")

    def test_search_enemy(self):
        model = PrimaVita(log_dir_info="test", params_dic={"initial_population": 3})

        # Test dead player
        model.players[0] = 1

        player = model.search_enemy(model.players[0])
        self.assertEqual(player, -1)

        # Test find opponent in radius
        model.players = [Player(i=0, log_dir="Players_Data_test", tob=10, x=50, y=500, energy=200),
                         Player(i=1, log_dir="Players_Data_test", tob=12, x=40, y=530, energy=200),
                         Player(i=2, log_dir="Players_Data_test", tob=12, x=48, y=505, energy=200)]

        player = model.search_enemy(model.players[0])
        self.assertEqual(player, 2)

        shutil.rmtree("Players_Data_test")

    def test_check_particles(self):
        model = PrimaVita(log_dir_info="test")

        model.food_particles = [Particle(x=64, y=514), Particle(x=10, y=502),
                                Particle(x=60, y=514), Particle(x=12, y=502)]
        model.check_particles()

        self.assertEqual(model.food_particles[2], 0)
        self.assertEqual(model.food_particles[3], 0)

        shutil.rmtree("Players_Data_test")

    def test_regenerate_species(self):
        model = PrimaVita(log_dir_info="test")

        model.regenerate_species()
        self.assertEqual(len(model.players), 20)

        shutil.rmtree("Players_Data_test")

    def test_take_action(self):
        model = PrimaVita(log_dir_info="test")

        

        shutil.rmtree("Players_Data_test")
