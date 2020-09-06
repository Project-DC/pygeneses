
# PyGeneses

[![GitHub](https://img.shields.io/github/license/Project-DC/pygeneses)](https://github.com/Project-DC/pygeneses/blob/master/LICENSE)  ![GitHub stars](https://img.shields.io/github/stars/Project-DC/pygeneses?style=plastic)  ![GitHub contributors](https://img.shields.io/github/contributors/Project-DC/pygeneses)  ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)  ![GitHub last commit](https://img.shields.io/github/last-commit/Project-DC/pygeneses)

<p align="justify">PyGeneses is a PyTorch based Deep Reinforcement Learning framework that helps users to simulate artificial agents in bio-inspired environments. The framework provides in-built Deep RL algorithms and visualization of results from training in an interactive dashboard. The environments are a simplified abstraction of our real world, agents are put into this world and are allowed to interact with each other and the environment.</p>

The power of PyGeneses is its clean and simple API which:
- Allows a user to run own simulation even if they have no knowledge about RL or DL.
- Allows a user with experience in Deep RL to tweak the model and parameters extensively.
<p align="justify">What’s exciting about PyGeneses you ask, well, PyGeneses lets you create a working simulation by writing as little as 2 lines without any prerequisite knowledge whatsoever!! PyGeneses also provides tools that will help you visualize the results with minimal effort. So what are you waiting for, install PyGeneses today and become the god of your creation</p>

## Prima vita

<p align="justify">Prima vita is a species of artificially simulated beings created as part of Project DC. This repository holds a simulation environment created in pygame which is to be used with Deep Reinforcement Learning algorithms to find out the evolution of Prima Vita.</p>

## Installation

PyGeneses can be installed using pip in either your local system or a cloud based platform. The steps for installation will be the same for both cloud and own systems.

```bash
user@programmer~:$ pip install git+https://github.com/Project-DC/pygeneses
```

<p align="justify">Running VitaBoard (an interactive dashboard to visualize Training results) requires a small python script. We recommend keeping this in an accessible location and using it to start the VitaBoard server everytime you need to visualize your results.
Open a text editor and type the following:-</p>

```bash
from pygeneses.vitaboard import run_board

run_board()
```

## About the packages   
<p align="justify">As of version 0.1-beta, the architecture of PyGeneses is built around 4 major modules. Each of these modules provides a unique feature or functionality to the framework. So, let’s get started with a brief introduction to each of them.</p>      

1. envs    
<p align="justify">This module allows you to create, configure and tweak the in-built bio-inspired environments. As of now, this only provides a single environment called Prima Vita (First Life), but there’s more coming soon! This lets you set up the entire environment and the species in just a few lines of code and provides both high level API and low level control over the environment. Training using the API includes logging of every action of an agent so that it can be studied using VitaBoard.</p>   

2. models   
<p align="justify">The ‘models’ module is what allows us to import the neural networks which the species uses to learn what to do. As of now, only the default model's (REINFORCE) implementation is provided, but we will be adding support for custom pluggable networks from v0.2 onwards.</p>

3. hypertune    
<p align="justify">The ‘HyperTune’ package allows us to configure and test out various hyperparameters we can provide for an environment and species (a list of hyperparameters is provided in the Classes section of this documentation). This contains single hyperparameter testing, grid search and randomized search. This allows us to find the best set of hyperparameters to display a type of behavior. This also produces logs which we can study using Vitaboard.</p>

4. vitaboard   
<p align="justify">Vitaboard provides an advanced, interactive dashboard to study agents after the training phase. After each agent dies, his/her actions are written into a log file. And vitaboard allows us to visualize the agent's life. It provides us with a life visualizer, group statistics and a genetic history visualizer. It allows us to identify and understand behaviours exhibited by an agent while interacting with the environment or with other agents in the environment.</p>

## Contributing

The following resources are a good place to get to know more about PyGeneses:-

1.  Introduction to PyGeneses  [Dev.to](https://dev.to/projectdc/introduction-to-pygeneses-26oc),  [Medium](https://medium.com/oss-build/introduction-to-pygeneses-1ed08a1a076c).
2.  Getting Started with PyGeneses [Dev.to](https://dev.to/projectdc/getting-started-with-pygeneses-1co2),  [Medium](https://medium.com/oss-build/getting-started-with-pygeneses-839ff6b3023f).
3. Studying logs using VitaBoard [Dev.to](https://dev.to/projectdc/guidelines-about-vitaboard-2m36), [Medium](https://medium.com/oss-build/studying-logs-using-vitaboard-41e13e3197d7)

Apart from these blog posts, you can also checkout the  [official docs](https://project-dc.github.io/docs).

Before moving further please go through the rules in  [CONTRIBUTING.md](./CONTRIBUTING.md)

## License

PyGeneses is licensed under GNU GPL v3 [LICENSE](./LICENSE)
