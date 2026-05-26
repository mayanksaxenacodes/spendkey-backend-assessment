#!/bin/bash
set -o errexit

psql -v ON_ERROR_STOP=1 --user "${POSTGRES_USER}" --dbname "spendkey" <<-EOSQL
BEGIN;
CREATE SCHEMA Authors;
CREATE SCHEMA Publishers;
CREATE SCHEMA Books;

CREATE TABLE Authors.Author (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE Publishers.Publisher (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE Books.Book (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name TEXT NOT NULL,
    description TEXT,
    isbn TEXT,
    tags TEXT[],
    price INT,
    ai_summary TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    author_id INT,
    publisher_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY(author_id) REFERENCES Authors.author(id),
    FOREIGN KEY(publisher_id) REFERENCES Publishers.Publisher(id)
);

INSERT INTO Publishers.publisher (name) VALUES ('Harper Colins'), ('Microsoft'), ('Manning');
INSERT INTO Authors.Author (name) VALUES ('J.R.R Tolkien'), ('Charles Petzold'), ('Tim McNamara');
INSERT INTO Books.Book (name, description, isbn, tags, price, author_id, publisher_id)
VALUES
(
    'The Silmarillion',
    'The Silmarilli were three perfect jewels created by Feanor, most gifted of the High Elves. When the first Dark Lord, Morgoth, stole the jewels and set them within an iron crown in the impenetrable fortress of Angband, Feanor and his kindred took up arms against the gos and waged a long and terrible war to recover them. This is the story of the heroism of Elves and Men in the First Age of Middle-earth, the foundations of the world and its peoples before the great events recorded in The Hobbit and The Lord of the Rings.',
    '978-0-00-752322-1',
    '{"fantasy","masterwork","wizards","fiction"}',
    999,
    1,
    1
),
(
    'Code',
    'Computers are everywhere — most obviously in our laptops and smartphones, but also our cars, televisions, microwave ovens, alarm clocks, robot vacuum cleaners, and other smart appliances. Have you ever wondered what goes on inside these devices to make our lives easier but occasionally more infuriating?',
    '978-0-13-790910-0',
    '{"computers", "electronics", "technology", "engineering"}',
    3699,
    2,
    2
),
(
    'Rust in Action',
    'Rust is the perfect language for systems programming. It delivers the low-level power of C along with rock-solid safety features that let you code fearlessly. Ideal for applications requiring concurrency, Rust programs are compact, readable, and blazingly fast. Best of all, Rusts famously smart compiler helps you avoid even subtle coding errors.',
    '978-1-61729-455-6',
    '{"computers", "software", "programming", "engineering"}',
    5899,
    3,
    3
);
COMMIT;
EOSQL
