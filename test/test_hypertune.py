import unittest
import shutil

from pygeneses.hypertune import HyperTune

class TestHyperTuneClass(unittest.TestCase):
    def test_hypertuner_grid_search(self):
        tuner = HyperTune(model_class='PrimaVita',
                          hyperparameters=['initial_population', 'initial_energy'],
                          values=[[50], [10]], stop_at=20)
        tuner.hypertuner()

        shutil.rmtree('Players_Data_initial_population_50_initial_energy_10')
