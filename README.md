# Mealbase
Mealbase is an application for generating meal suggestions and other
curious statistics about the foods you eat.

## Overview
### The core idea
- The user logs the foods they eat, constantly adding to the database of meals.
  - All meals are comprised of ingredients. For each meal, the user inputs at least the
main ingredients.
    - i.e. meatballs and spaghetti -> meat, pasta. Chicken soup -> chicken, potatoes.
- Based on this constantly growing reord of meals, mealbase tries to suggest foods
that keep your menu diverse.
  - Recommendations are done based on ingredients. Say the user has recently logged
meatballs and spaghetti and chicken soup as eaten meals. Thus, Meat, chicken, pasta and
potatoes are ingredients mealbase tries to avoid when recommending the next meal.
  - The recommendation will most likely be in the form of the ingredients deemed
fitting. Additionally, if meals containing those ingredients are found in the database,
they could also be offered as suggestions here.
- Mealbase can of course also provide additional insights based on the data - for
example how the consumption of a certain ingredient changes in time or what was the most
popular meal in a given year etc.

### Possible problems
- The main issue with this idea is that the user starts with an empty database.
  - The recommendations won't make sense, and there is not much insight to gather from
a few ingredients.
  - In a way this could be mitigated by providing some ingredients pre-added into the
database.
    - This means mealbase can always recommend something, even on first log.
    
## Initial feature ideas
### The core features
At least these are needed to implement the core idea of the app
- Users: There should be users, and each user should only be able to see and add to
their own data. To have users, a functionality for creating a user account is needed, as
well as a login / logout.
- Logging meals: To have the app work in any way, a page for logging foods is essential.
- Recommendations: A page on which the user can see recommendations on what to eat next.
- Additional statistics: A page for displaying additional statistics / redirecting to
other pages with additional statistics.

### Additional features
These are some additional ideas:
- Blacklist: Maybe a user tries a new meal or an ingredient but doesn't like it.
A functionality to "blacklist" it so mealbase won't recommend it anymore could be
useful.
- User roles: An admin role with access to every user's data and additional operations
(for example deleting data).
- Recipes: Each meal could have a recipe too.
- Shopping lists: If we have recipes, we could probably generate a shopping list from a
meal suggestion.
