CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE meals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    name TEXT UNIQUE
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    name TEXT UNIQUE
);

CREATE TABLE meal_ingredients (
    id SERIAL PRIMARY KEY,
    meal_id INTEGER REFERENCES meals,
    ingredient_id INTEGER REFERENCES ingredients
);

CREATE TABLE meal_log (
    id SERIAL PRIMARY KEY,
    date DATE,
    meal_id INTEGER REFERENCES meals
);
