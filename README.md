# Vote for a Movie API
An API server implemented in Flask backed by MongoDB.
The first try to organize teamwork.

## Technologies
![Flask, Flask REST-Plus, MongoEngine](https://user-images.githubusercontent.com/43119488/62832713-91fed480-bc3b-11e9-890f-43337a6dbc1a.jpg)

## Setup

A MongoDB server is supposed to be running at ```localhost:27017```.

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ export FLASK_APP=app.py FLASK_ENV=development
$ python -m flask run
```

## Usage

First of all, go to ```http://localhost:5000/api/v1/``` in your browser.
You should get a Swagger UI then.

Movie objects have the next structure in JSON:

```json
{
  "id": "5d3c35189775d4a2a1d4bd65",
  "title": "Terminator",
  "releaseDate": "1984-10-26",
  "actors": [
    "Arnold"
  ],
  "genres": [
    "Action",
    "Sci-Fi"
  ],
  "sumOfMarks": 260,
  "numberOfMarks": 3
}
```

### Observe the movies database

* ```/api/v1/movies/``` to get all movies
* ```/api/v1/movies/?title_contains=rEst``` to filter by a title's
case-insensitive substring
* ```/api/v1/movies/?actor=Evan&actor=Arnold``` to get movies either with
Evan or Arnold (not and)
* ```/api/v1/movies/?genre=Action&genre=Sci-Fi```
* ```/api/v1/movies/?actor=Tom&genre=Drama&title_contains=ReSt```

### ```POST``` a voting

Request body:

```json
{
  "choices": [
    {
      "title": "Terminator"
    },
    {
      "title": "Forrest Gump"
    }
  ],
  "maxVotes": 3
}
```

Additionally, ```startDate``` and ```finishDate``` can be specified.
All these fields including ```maxVotes``` are optional.

Response body:

```json
{
  "id": "5d4e8fe2e67369592e1bbd4b",
  "choices": [
    {
      "id": "5d4e8fe2e67369592e1bbd49",
      "title": "Terminator",
      "votes": 0
    },
    {
      "id": "5d4e8fe2e67369592e1bbd4a",
      "title": "Forrest Gump",
      "votes": 0
    }
  ],
  "currentVotes": 0,
  "maxVotes": 3,
  "startDate": null,
  "finishDate": null
}
```

### ```GET``` the created voting

Use the voting's ```id```:

```/api/v1/votings/5d4e8fe2e67369592e1bbd4b```

Share the link with your friends.

### Vote for a movie

Use a choice's ```id``` from the ```choices``` array:

```
POST /api/v1/votings/5d4e8fe2e67369592e1bbd4b/choices/5d4e8fe2e67369592e1bbd49/actions/

{
  "type": "vote"
}
```

Server responses with 204 if your vote is successfully accounted.

### Go to the cinema with your friends

Just do it.

### Rate for the movie you've watched

Send your mark from 1 to 100:

```
POST /api/v1/movies/5d3c35189775d4a2a1d4bd65/actions/

{
  "type": "rate",
  "data": {
    "mark": 75
  }
}
```
