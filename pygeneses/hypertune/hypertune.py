# Hyperparameter tuning package

# Import required libraries
import importlib
import itertools
import math
import random

# Import required environment class
class_import = {
    "PrimaVita": importlib.import_module("pygeneses.envs.prima_vita").PrimaVita
}


class HyperTune:
    """
    HyperTune class for hyperparameter tuning

    Data members
    ============
    model_class    (str)
        : Name of model environment to tune hyperparameters for
    hyperparameter (str)
        : Hyperparameter to tune
    values         (list)
        : Value list which should be checked with current hyperparameter
    stop_at        (int)
        : Approximate number of logs to be generated
    """

    def __init__(
        self, model_class, hyperparameters, values, stop_at, randomize_percent=1
    ):
        """
        Initializer for HyperTune class

        Params
        ======
        model_class    (str)
            : Name of model environment to tune hyperparameters for
        hyperparameters (str)
            : Hyperparameters to tune
        values         (list)
            : Value list which should be checked with current hyperparameter
        stop_at        (int)
            : Approximate number of logs to be generated
        """

        self.model_class = model_class
        self.hyperparameters = hyperparameters
        self.values = values
        self.stop_at = stop_at
        self.randomize_percent = randomize_percent

    def hypertuner(self):
        """
        Runs environment with every value of hyperparameter specified
        """

        cross_product = list(itertools.product(*self.values))
        cross_product = random.sample(
            cross_product, k=math.ceil(self.randomize_percent * len(cross_product))
        )

        print("Training on", len(cross_product), "combinations!")

        for i in range(len(cross_product)):
            log_dir_info = ""
            params_dic = {}
            for j in range(len(self.hyperparameters)):
                params_dic[self.hyperparameters[j]] = cross_product[i][j]
                log_dir_info += (
                    str(self.hyperparameters[j]) + "_" + str(cross_product[i][j]) + "_"
                )

            object = class_import[self.model_class](
                params_dic=params_dic, log_dir_info=log_dir_info[:-1]
            )
            print("-" * 100)
            print(params_dic)
            print("-" * 100)
            object.run(stop_at=self.stop_at)
