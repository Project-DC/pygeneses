from pygeneses.envs.prima_vita import PrimaVita

rl_model = PrimaVita(initial_population=10, log_dir_info="profile")
rl_model.run(stop_at=20)
