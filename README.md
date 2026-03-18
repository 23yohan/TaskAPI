# TaskAPI Project

## Overview
This project goal is to create a backend for a task application where users can create, modify and store tasks. This is created with a using a Flask framework with a postgreSQL database. 

## Installation
The project depends on a number of python modules outlined in the ```requirements.txt``` file. In addition to this, the following dependencies are required
- Docker
- Kubernetes
- Postgres (psql CLI)

### Without docker
If you want to run the project without docker, you can use a python virtual environment and host the postgres database in a docker container. From the project root, run the following commands
```
$ python3 -m venv .venv/
$ source .venv/bin/activate
(.venv) $ pip install -r requirements.txt

# Set up database
(.venv) $ flask db init
(.venv) $ flask db migrate -m "Migrating DB schema"
(.venv) $ flask db upgrade
(.venv) $ docker-compose up db

# Start application
(.venv) $ flask run
```

## Future Tasks
There is more work to be done in this project to be deemed complete. This is a live list that will change over time.
- API Developement
  - Add rate limiting on API calls
  - Add endpoints for creating users
  - Add endpoint authentication for specific users
    - Users can only modify/delete tasks assigned to them
- Unit Testing
    - creating unit tests for bad inputs/responses
- Frontend development
- Deployment on AWS platform 