CREATE DATABASE IF NOT EXISTS canvas_ai
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE canvas_ai;

-- login
CREATE TABLE login (
    account_id  BIGINT UNSIGNED PRIMARY KEY,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- session
CREATE TABLE session (
    session_id     INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    account_id     BIGINT UNSIGNED NOT NULL,
    session_title  VARCHAR(255) NOT NULL,
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_session_account
        FOREIGN KEY (account_id) REFERENCES login(account_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- chat
CREATE TABLE chat (
    chat_id      INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    session_id   INT UNSIGNED NOT NULL,
    message      JSON NOT NULL,
    response     JSON,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_chat_session
        FOREIGN KEY (session_id) REFERENCES session(session_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- indexes
CREATE INDEX idx_session_account_id ON session(account_id);
CREATE INDEX idx_chat_session_id ON chat(session_id);

-- hey there!