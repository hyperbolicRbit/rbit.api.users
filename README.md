# Users Microservice

## What do you need

### Docker-ce

**Version:** Docker version 17.09.1-ce, build 19e2cf6
Downlad from [here](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/)

### Docker-compose

**Version:** docker-compose version 1.18.0-rc2, build 189468b
Download from [here](https://docs.docker.com/compose/install/)

### Docker-machine

**Version:** docker-machine version 0.13.0, build 9ba6da9
Download from [here](docker-machine version 0.13.0, build 9ba6da9)


## Workflow

### VirtualEnv

```bash
$ python3.6 -m venv env
$ source env/bin/activate
```

### Docker common commands

Build the images:
```bash
$ docker-compose build
```

Run the containers:
```bash
$ docker-compose up -d
```

Create the database:
```bash
$ docker-compose run users-service python manage.py recreate_db
```

Seed the database:
```bash
$ docker-compose run users-service python manage.py seed_db
```

Run the tests:
```bash
$ docker-compose run users-service python manage.py test
```

#### Deploy to production with AWS

Create aws host:
```bash
docker-machine create --driver amazonec2 --amazonec2-access-key <key> --amazonec2-secret-key <secresecrett> aws
```

Active host and point the docker client at it:
```bash
$ docker-machine env aws
$ eval $(docker-machine env aws)
```

List running machines setting timeout to 60 seconds:
```bash
$ docker-machine ls -t 60
```

Spin up the containers, create the database, seed, and run the tests:
```bash
$ docker-compose -f docker-compose-prod.yml up -d --build
$ docker-compose -f docker-compose-prod.yml run users-service python manage.py recreate_db
$ docker-compose -f docker-compose-prod.yml run users-service python manage.py seed_db
$ docker-compose -f docker-compose-prod.yml run users-service python manage.py test
```

### Postgres

Access the database via psql:
```bash
$ docker exec -ti users-db psql -U postgres -W
```

Then, you can connect to db and run SQL queries:
```bash
# \c users_dev
# select * from users;
```

### Environment variables development environment

```bash
$ source env/bin/activate
export REACT_APP_USERS_SERVICE_URL=http://127.0.0.1:5000
export APP_SETTINGS=project.config.DevelopmentConfig
export DATABASE_URL=postgres://postgres:postgres@localhost:5432/users_dev
export DATABASE_TEST_URL=postgres://postgres:postgres@localhost:5432/users_test
export SECRET_KEY=my_precious
export TEST_URL=http://localhost
python manage.py test
cd ../flask-microservices-main
testcafe chrome e2e
```

### Flask Migrator

#### Change the model and migrate:

```bash
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

#### Start local flask

```bash
$ python manage.py runserver
```

### React

#### Start local react

```bash
$ export REACT_APP_USERS_SERVICE_URL=http://127.0.0.1:5000
$ npm start
```

### Setting up local environment

1. Install postgres
2. Set default password to postgres
```bash
$ sudo -u postgres psql
$ \password postgres
$ \q
```
3. Uninstall and install psycopg2
```bash
$ pip uninstall psycopg2
$ pip install psycopg2 --upgrade
```
4. Set environment variables
5. Run manage.py recreate_db seed_db & test / cov
