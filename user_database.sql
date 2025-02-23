CREATE TABLE IF NOT EXISTS user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    github TEXT,
    linkedin TEXT,
    projects TEXT,
    classes TEXT,
    other TEXT
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES user_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT,
    FOREIGN KEY (user_id) REFERENCES user_profiles(id) ON DELETE CASCADE
);
