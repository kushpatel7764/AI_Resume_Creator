CREATE TABLE IF NOT EXISTS user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_name TEXT NOT NULL,
    user_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    github TEXT,
    linkedin TEXT,
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

UPDATE user_profiles
SET other = 'Programing languages:  Python, Java, Swift, and JavaScript. I also MySQL from my database system course. ' ||
            'Tools: Git, JetBrain IDEs, Xcode, and Vscode ' ||
            'Awards:  I was awarded Dr. Linda Wilkens and Dr. Glenn Pavlicek Scholarship at BSU in recognition of my academic achievements such as a 4.0 major GPA. I also a google software development certificate and I.T. support certificate.' ||
            'School: I am a computer science major studying at Bridgewater State University (BSU), I am driven by a desire to innovate and problem solve. I am graduating from the BSU on May, 2025.' ||
            'About me: I am from East Greenwich, Road Island but I currently live in Fairhaven, Massachusetts.'

WHERE id = 2;