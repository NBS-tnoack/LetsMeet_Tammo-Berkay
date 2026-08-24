DROP VIEW IF EXISTS migration_users;
DROP TABLE IF EXISTS migration_persons;

CREATE TABLE migration_persons (
    person_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email text NOT NULL UNIQUE CHECK (email <> ''),
    first_name text NOT NULL,
    last_name text NOT NULL,
    birth_date date NOT NULL,
    postal_code text NOT NULL,
    city text NOT NULL
);

CREATE VIEW migration_users (email, first_name, last_name, birth_date, postal_code, city) AS
SELECT email, first_name, last_name, birth_date, postal_code, city
FROM migration_persons;
