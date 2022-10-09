# Mealbase
Mealbase is an application for generating food suggestions about the meals you eat. Try
it on [heroku](https://tsoha-mealbase.herokuapp.com/) (but read this readme first!)

## The idea
- The user logs the meals they eat.
  - All meals are comprised of ingredients. For each meal, the user inputs at least the
main ingredients.
    - i.e. meatballs and spaghetti -> meat, pasta. Chicken soup -> chicken, potatoes.
- Based on the record of meals, mealbase tries to suggest foods that keep your menu
diverse. 
  - Recommendations are done based on ingredients and logging dates. Currently mealbase
suggests ingredients based on the number of days since they have last been logged. The
longer the time since last eaten, the higher the priority for suggesting.

## Features
The current status of features:
### Core features
- [x] Creating user accounts
- [x] A login / logout
- [x] A page for logging foods: Works, but logging meals could be separated from logging
ingredients, since if a meal is already in the database, ingredients are not needed.
- [x] A page for viewing the meal log
- [x] A page for viewing logged ingredients
- [x] A page with recommendations: Currently a fixed number of 4 ingredients is
suggested, could be more dynamic
- [x] Situational error messages and redirecting from errors
- [ ] Nicer UI

### Additional features
- [ ] Additional suggestion methods
- [ ] A page for displaying additional statistics / redirecting to other pages with
additional statistics.
- [ ] User roles: An admin role with access to additional operations.
> **Note** at the moment when creating an account role selection is available, but it
does not do anything.
- [ ] Blacklist: Maybe a user tries a new meal or an ingredient but doesn't like it.
A functionality to "blacklist" it so mealbase won't recommend it anymore could be
useful.
- [ ] Recipes: Each meal could have a recipe too.
- [ ] Shopping lists: If we have recipes, we could probably generate a shopping list
from a meal suggestion.

## Architechture
```
mealbase
├── schema.sql  # Database schema
├── config.py   # Access to env variables
├── app.py      # App creation
├── db.py       # Database creation
├── routes.py   # Routes
├── log.py      # High level functions for accessing the meal log. Used by routes.py
├── users.py    # High level Functions for accessing the users. Used by routes.py
├── queries     # A package for the code directly interacting with the database
│   ├── log_queries.py   # Queries for accessing the log. Used by log.py
│   └── user_queries.py  # Queries for accessing the users. Used by users.py
└── templates  # The templates
    ├── error.html
    ├── index.html
    ├── ingredients.html
    ├── log_meal.html
    ├── login.html
    ├── meal_log.html
    ├── register.html
    └── suggestions.html
```

## Setup
### Setting up a local database container
Start the service:
```console
docker compose up -d
```

Open a bash shell to the container:
```console
docker exec -it postgres bash
```

Set up the tables:
```console
psql -U postgres_user postgres_db < schema.sql
```

### Deploying to heroku
Setup heroku database from container:
```console
heroku psql < schema.sql --app tsoha-mealbase
```
