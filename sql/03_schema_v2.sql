DROP VIEW IF EXISTS migration_messages;
DROP VIEW IF EXISTS migration_likes;
DROP VIEW IF EXISTS migration_user_hobbies;
DROP VIEW IF EXISTS migration_user_interests;
DROP VIEW IF EXISTS migration_users;
DROP TABLE IF EXISTS migration_messages_data;
DROP TABLE IF EXISTS migration_likes_data;
DROP TABLE IF EXISTS migration_hobbies_data;
DROP TABLE IF EXISTS migration_interests_data;
DROP TABLE IF EXISTS migration_persons;

CREATE TABLE migration_persons (
    person_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email text NOT NULL UNIQUE CHECK (email <> ''),
    first_name text NOT NULL,
    last_name text NOT NULL,
    birth_date date NOT NULL,
    postal_code text NOT NULL,
    city text NOT NULL,
    phone text NOT NULL,
    gender text NOT NULL
);

CREATE TABLE migration_interests_data (
    person_id integer NOT NULL REFERENCES migration_persons(person_id),
    interest_code text NOT NULL,
    PRIMARY KEY (person_id, interest_code)
);

CREATE TABLE migration_hobbies_data (
    person_id integer NOT NULL REFERENCES migration_persons(person_id),
    hobby_name text NOT NULL,
    priority integer NOT NULL CHECK (priority BETWEEN -100 AND 100),
    source text NOT NULL,
    PRIMARY KEY (person_id, hobby_name, source)
);

CREATE TABLE migration_likes_data (
    liker_id integer NOT NULL REFERENCES migration_persons(person_id),
    liked_id integer NOT NULL REFERENCES migration_persons(person_id),
    status text NOT NULL,
    liked_at timestamp NOT NULL,
    PRIMARY KEY (liker_id, liked_id, liked_at)
);

CREATE TABLE migration_messages_data (
    sender_id integer NOT NULL REFERENCES migration_persons(person_id),
    receiver_id integer NOT NULL REFERENCES migration_persons(person_id),
    body text NOT NULL,
    sent_at timestamp NOT NULL,
    conversation_id integer NOT NULL,
    PRIMARY KEY (sender_id, receiver_id, sent_at, conversation_id)
);

CREATE VIEW migration_users (email, first_name, last_name, birth_date, postal_code, city, phone, gender) AS
SELECT email, first_name, last_name, birth_date, postal_code, city, phone, gender
FROM migration_persons;

CREATE VIEW migration_user_interests (email, interest_code) AS
SELECT p.email, i.interest_code
FROM migration_interests_data i
JOIN migration_persons p ON p.person_id = i.person_id;

CREATE VIEW migration_user_hobbies (email, hobby_name, priority, source) AS
SELECT p.email, h.hobby_name, h.priority, h.source
FROM migration_hobbies_data h
JOIN migration_persons p ON p.person_id = h.person_id;

CREATE VIEW migration_likes (liker_email, liked_email, status, liked_at) AS
SELECT liker.email, liked.email, l.status, l.liked_at
FROM migration_likes_data l
JOIN migration_persons liker ON liker.person_id = l.liker_id
JOIN migration_persons liked ON liked.person_id = l.liked_id;

CREATE VIEW migration_messages (sender_email, receiver_email, body, sent_at, conversation_id) AS
SELECT sender.email, receiver.email, m.body, m.sent_at, m.conversation_id
FROM migration_messages_data m
JOIN migration_persons sender ON sender.person_id = m.sender_id
JOIN migration_persons receiver ON receiver.person_id = m.receiver_id;
