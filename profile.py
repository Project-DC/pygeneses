import os

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.environ["SDL_VIDEODRIVER"] = "dummy"

from pygeneses.envs.prima_vita import PrimaVita

rl_model = PrimaVita()

def training_loop(n_episodes=1000, max_t=1000, gamma=1.0, print_every=100):
    rl_model.init()

    states = rl_model.get_current_state()

    running = True
    while running:
        rl_model.update_time()
        if(rl_model.time == 60):
            running = False
        elif(rl_model.time % 10 == 0):
            print("\U0001F552 Time:", rl_model.time)
        for i, agent in enumerate(rl_model.model.agents):
            if(type(rl_model.players[i]) != int):
                rl_model.take_action(i, states[i])

                states = rl_model.get_current_state()
                if(type(states) == int and states == -1):
                    running = False

training_loop()
