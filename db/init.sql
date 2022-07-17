CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS UserFiles (
    user_id INTEGER,
    hash TEXT UNIQUE NOT NULL,
    path TEXT UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE,
    UNIQUE(user_id, hash)
);

INSERT OR IGNORE INTO Users (username, password) values ('admin', 'admin');
INSERT OR IGNORE INTO Users (username, password) values ('user', '1111');
