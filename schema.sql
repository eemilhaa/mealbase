CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    role INTEGER
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
    meal_id INTEGER REFERENCES meals,
    ingredient_id INTEGER REFERENCES ingredients
);

CREATE TABLE meal_log (
    date DATE,
    meal_id INTEGER REFERENCES meals
);
