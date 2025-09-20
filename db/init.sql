DROP TABLE IF EXISTS colleges CASCADE;

DROP TABLE IF EXISTS programs CASCADE;

DROP TABLE IF EXISTS students CASCADE;

CREATE TYPE year_level_enum AS ENUM ('1st', '2nd', '3rd', '4th', '4th+');

CREATE TYPE gender_enum AS ENUM ('male', 'female', 'others', 'prefer not to say');

CREATE TABLE IF NOT EXISTS colleges (
    college_code VARCHAR(32) NOT NULL PRIMARY KEY,
    college_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS programs (
    program_code VARCHAR(32) NOT NULL PRIMARY KEY,
    program_name TEXT NOT NULL UNIQUE,
    college_code TEXT REFERENCES colleges (college_code) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS students (
    id_number CHAR(9) NOT NULL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    year_level year_level_enum NOT NULL,
    gender gender_enum NOT NULL,
    program_code TEXT REFERENCES programs (program_code) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT unique_full_name UNIQUE (first_name, last_name)
);

CREATE TABLE users (
    user_id UUID NOT NULL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE INDEX idx_programs_college ON programs (college_code);

CREATE INDEX idx_students_program ON students (program_code);