# flask-backlog-api
A Flask-based RESTful API that leverages flask-jwt-extended to handle backlog activites for multiple users

<b>Requirements:</b>
* Python3
* pipenv (unless you want to install the minimal dependencies manually or using pip)

https://github.com/pypa/pipenv

* Redis

https://redis.io/topics/quickstart

<b>Installation</b>
1. Inside repo, run `pipenv shell` to initialize a pipenv environment
2. Run `pipenv install` to install dependencies inside Pipfile
3. `python run.py` and it should be running at default `localhost:5000`

<b>Database Initialization</b>
1. Enter the python shell with `python`
2. Import the database from the app with `from app import db`
3. Run the database create function: `db.create_all()`

<b>Starting Redis</b>
1. After installation, run `redis-server` and it should now start as a system service
2. Start the default redis queue on a separate terminal from the main application by running `rq worker` 
  It should display `*** Listening on default...`
3. Try hitting the `/register` endpoint and observe the redis terminal.
<h3>Major Endpoints</h3>

`/register`
`POST`

Creates new User

``` js
{
  "username"
  "password"
  "email"
}
```

`/login`
`POST`

Authenticates user and returns JWT

``` js
{
  "username"
  "password"
}
```

`/user/<id>`
`GET`

Returns a user based on id

`/user/activity/new` 
`POST`

Creates new user activity

``` js
{
  "activity_type"
  "name"
  "desc"
}
```

`/user/activity` 
`GET`

Returns all activites of a user

`/activity/episode/<id>`
`POST`

Extends an Activity with the Episode class

``` js
{
  "episode_total"
  "episode_progress"
}
```

`/user/activity/edit/<id>`
`PUT`

Edits both an activty and/or episodes. This allows the user to mark the activity as complete or update episode progress

``` js
{
  "activity_type"
  "name"
  "desc"
  "episode_total"
  "episode_progress"
}
```
