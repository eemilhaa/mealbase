# Mealbase
Mealbase is an application for generating food suggestions about the meals you eat. ~~Try
it on [heroku](https://tsoha-mealbase.herokuapp.com/).~~ Heroku free was cancelled and thus
this app is no longer available there.

## How it works
- The user logs the meals they eat.
  - All meals are comprised of ingredients. For each meal, the user inputs at least the
main ingredients.
    - i.e. meatballs and spaghetti -> meat, pasta. Chicken soup -> chicken, potatoes.
- Based on the record of meals, mealbase tries to suggest foods that keep your menu
diverse. 
  - Recommendations are done based on ingredients and logging dates. Mealbase suggests
ingredients based on the number of days since they have last been logged - the longer
the time since last eaten, the higher the priority for suggesting.
  - The user can query the database for meals containing the suggested ingredients.

## Features
All planned core features have been implemented:
- [x] Creating user accounts
- [x] A login / logout
- [x] A page for logging meals
- [x] A page for logging ingredients when needed
- [x] A page for viewing the meal log
- [x] A page for viewing logged ingredients
- [x] A page with ingredient suggestions
- [x] Links from the suggestions page to meals that contain the suggested ingredients
- [x] Situational error messages
- [x] Clean UI

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
    ├── index.html
    ├── ingredients.html
    ├── layout.html
    ├── logging.html
    ├── login.html
    ├── meal_log.html
    ├── meals_with_ingredient.html
    ├── register.html
    └── suggestions.html
```

## Development
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
