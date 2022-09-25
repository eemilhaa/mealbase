# Mealbase
Mealbase is an application for generating meal suggestions about the foods you eat. Try
it on [heroku](https://tsoha-mealbase.herokuapp.com/) (but read this readme first!)

## The idea
- The user logs the meals they eat.
  - All meals are comprised of ingredients. For each meal, the user inputs at least the
main ingredients.
    - i.e. meatballs and spaghetti -> meat, pasta. Chicken soup -> chicken, potatoes.
- Based on the record of meals, mealbase tries to suggest foods that keep your menu
diverse. 
> **Note** the suggestion logic has not yet been implemented.
  - Recommendations are done based on ingredients. Say the user has recently logged
meatballs and spaghetti and chicken soup as eaten meals. Thus, Meat, chicken, pasta and
potatoes are ingredients mealbase tries to avoid when recommending the next meal.
  - The recommendation will most likely be in the form of the ingredients deemed
fitting. Additionally, if meals containing those ingredients are found in the database,
they could also be offered as suggestions here.
- Mealbase could also provide additional insights based on the data - for example how
the consumption of a certain ingredient changes in time or what was the most popular
meal in a given year etc.

## Features
The current status of features is tracked here. At this point a checked box means the
feature somewhat works, not that it is finished / polished.
### Core features
- [x] Creating user accounts
- [x] A login / logout
- [x] A page for logging foods
- [x] A page for viewing the meal log
- [x] A page for viewing logged ingredients
- [ ] A page with recommendations
- [ ] Situational error messages: For example, when creating a user account, if the
username is already taken, the app should tell the user about this. Currently it
just takes the user back to the initial login view.
- [ ] Nicer UI

### Additional features
- [ ] A page for displaying additional statistics / redirecting to other pages with
additional statistics.
- [ ] User roles: An admin role with access to additional operations.
> **Note** at the moment when creating an account role selection is available, but it
does not do anything
- [ ] Blacklist: Maybe a user tries a new meal or an ingredient but doesn't like it.
A functionality to "blacklist" it so mealbase won't recommend it anymore could be
useful.
- [ ] Recipes: Each meal could have a recipe too.
- [ ] Shopping lists: If we have recipes, we could probably generate a shopping list
from a meal suggestion.

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
