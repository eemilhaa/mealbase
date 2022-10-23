CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT
);

CREATE TABLE meals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    name TEXT
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE meal_ingredients (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    meal_id INTEGER REFERENCES meals,
    ingredient_id INTEGER REFERENCES ingredients
);

CREATE TABLE meal_log (
    id SERIAL PRIMARY KEY,
    date DATE DEFAULT NOW(),
    meal_id INTEGER REFERENCES meals
);
