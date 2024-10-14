CREATE TABLE events (
    id SERIAL PRIMARY KEY,              
    title VARCHAR(100) NOT NULL,
    date TIMESTAMP NOT NULL,
    description TEXT
);
