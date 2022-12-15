# Local Development Environment

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Structure](#structure)
- [Contributing](#contributing)

## About <a name = "about"></a>

Simple environment for running agent-based simulations.
The Local Development Environment is a part of the [Agents Assembly](https://agents-assembly.com) ecosystem.
Other applications are:
- [Simulation Run Environment](https://github.com/agent-base-information-flow-simulation/simulation-run-environment) - scalable run environment for Agents Assembly.
- [Local Interface](https://github.com/agent-based-information-flow-simulation/local-interface) - GUI for simulation definition, management, and analysis.
- [Communication Server](https://github.com/agent-based-information-flow-simulation/communication-server) - cluster of servers used for XMPP communication.
- [Agents Assembly Translator](https://github.com/agent-based-information-flow-simulation/agents-assembly-translator) - translator for Agents Assembly code.

## Getting Started <a name = "getting_started"></a>

### Prerequisites

```
docker
```

### Installing
To use the application, utilize the `server.sh` script. </br>
Install and start the application:
```
./server.sh start
```

To see all the available options run the `help` command:
```
./server.sh help
```

## Structure <a name = "structure"></a>

The structure of the simulation run environment is presented below.
- [Mongo](#mongo)
- [Mongo GUI](#mongo-gui)
- [SPADE instance](#spade-instance)
- [Translator](#translator)

### Mongo <a name = "mongo"></a>
The service is used as a general database.
It stores agents' updates coming from spade instances.

Environment variables:
* `MONGODB_ROOT_USER` - root user (i.e., root)
* `MONGODB_ROOT_PASSWORD` - root password (i.e., root)
* `MONGODB_USERNAME` - database user (i.e., user)
* `MONGODB_PASSWORD` - database password (i.e., pass)
* `MONGODB_DATABASE` - database name (i.e., simulations)

Host port mapping (dev only):
* `27017`

### Mongo GUI (dev only) <a name = "mongo-gui"></a>
The service provides a graphical user interface to access the data stored inside the timeseries database.

Environment variables:
* `ME_CONFIG_MONGODB_ADMINUSERNAME` - MongoDB root user (i.e., root)
* `ME_CONFIG_MONGODB_ADMINPASSWORD` - MongoDB root password (i.e., root)
* `ME_CONFIG_MONGODB_SERVER` - MongoDB address (i.e., mongo)
* `ME_CONFIG_OPTIONS_EDITORTHEME` - theme name (i.e., 3024-night)

Host port mapping (dev only):
* `27018`

### SPADE instance <a name = "spade-instance"></a>
The service translates and runs the received code.
It is responsible for generating the graph structure for agents.
It consists of Web API and the simulation process.
The latter one is created while starting the simulation.
The API is used to communicate and manage the instance.
The service sends the running agents' state updates to the Mongo service.

[Docker Hub](https://hub.docker.com/repository/docker/madpeh/lde-spade-instance)

Environment variables:
* `ACTIVE_SIMULATION_STATUS_ANNOUCEMENT_PERIOD` - active simulation process status announcement period (i.e., 10)
* `AGENT_BACKUP_PERIOD` - agent backup period (i.e., 10)
* `AGENT_BACKUP_DELAY` - agent first backup delay after starting (i.e., 5)
* `DB_URL` - database url (i.e., mongodb://user:pass@mongo:27017/simulations)
* `LOG_LEVEL_AGENT` - log level for agents running in the simulation process; see spade-instance/src/simulation/code_generation.py (i.e., INFO)
* `LOG_LEVEL_DB` - log level for database (i.e., INFO)
* `LOG_LEVEL_UVICORN_ACCESS` - log level for uvicorn server (i.e., INFO)
* `LOG_LEVEL_REPEATED_TASKS_SIMULATION` - log level for repeated tasks related to the simulation (i.e., INFO)
* `LOG_LEVEL_ROUTERS_SIMULATION` - log level for routers related to the simulation (i.e., INFO)
* `LOG_LEVEL_SIMULATION_CODE_GENERATION` - log level for spade-instance/src/simulation/code_generation.py (i.e., INFO)
* `LOG_LEVEL_SIMULATION_INITIALIZATION` - log level for spade-instance/src/simulation/initialization.py (i.e., INFO)
* `LOG_LEVEL_SIMULATION_MAIN` - log level for spade-instance/src/simulation/main.py (i.e., INFO)
* `LOG_LEVEL_SIMULATION_STATUS` - log level for spade-instance/src/simulation/status.py (i.e., INFO)
* `LOG_LEVEL_SPADE_BEHAVIOUR` - log level for SPADE behaviours (i.e., INFO)
* `LOG_LEVEL_STATE` - log level for spade-instance/src/state.py (i.e., INFO)
* `PORT` - listen port (i.e., 8000)
* `RELOAD` - reload application after detecting a change in source files (i.e., False); if set to True, it requires the following volume attached: spade-instance/src:/api/src
* `SIMULATION_PROCESS_HEALTH_CHECK_PERIOD` - running simulation health check period (i.e., 5)
* `WAIT_FOR_DB_ADDRESS` - Mongo address (i.e., mongo:27017)

Host port mapping (dev only):
* `8000`

### Translator <a name = "translator"></a>
The service's Web API enables the translation of Agents Assembly code using the `aasm` package.

[Docker Hub](https://hub.docker.com/repository/docker/madpeh/lde-translator)

Environment variables:
* `PORT` - listen port (i.e., 8000)
* `RELOAD` - reload application after detecting a change in source files (i.e., False); if set to True, it requires the following volume attached: translator/src:/api/src

Host port mapping (dev only):
* `8001`

## Contributing <a name = "contributing"></a>
Please follow the [contributing guide](CONTRIBUTING.md) if you wish to contribute to the project.
