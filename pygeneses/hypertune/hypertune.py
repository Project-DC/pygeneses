# Hyperparameter tuning package

# Import required libraries
import importlib

# Import required environment class
class_import = {"PrimaVita": importlib.import_module('pygeneses.envs.prima_vita').PrimaVita}

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

    def __init__(self, model_class, hyperparameter, values, stop_at):
        """
        Initializer for HyperTune class

        Params
        ======
        model_class    (str)
            : Name of model environment to tune hyperparameters for
        hyperparameter (str)
            : Hyperparameter to tune
        values         (list)
            : Value list which should be checked with current hyperparameter
        stop_at        (int)
            : Approximate number of logs to be generated
        """

        self.model_class = model_class
        self.hyperparameter = hyperparameter
        self.values = values
        self.stop_at = stop_at

    def hypertuner(self):
        """
        Runs environment with every value of hyperparameter specified
        """

        for value in self.values:
            params_dic = {self.hyperparameter: value}
            object = class_import[self.model_class](
                    params_dic=params_dic,
                    log_dir_info=self.hyperparameter + "_" + str(value)
            )
            print("-" * 100)
            print(" ".join(self.hyperparameter.split("_")).capitalize(), ": ", value)
            print("-" * 100)
            object.run(stop_at=self.stop_at)
