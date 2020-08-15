import importlib

class_import = {"PrimaVita": importlib.import_module('pygeneses.envs.prima_vita').PrimaVita}

class HyperTune:

    def __init__(self, model_class, hyperparameter, values, stop_at):
        self.model_class = model_class
        self.hyperparameter = hyperparameter
        self.values = values
        self.stop_at = stop_at

    def hypertuner(self):
        for value in self.values:
            object = class_import[self.model_class](log_dir_info=self.hyperparameter + "_" + str(value))
            setattr(object, self.hyperparameter, value)
            print("-" * 100)
            print(" ".join(self.hyperparameter.split("_")).capitalize(), ": ", value)
            print("-" * 100)
            object.run(stop_at=self.stop_at)
