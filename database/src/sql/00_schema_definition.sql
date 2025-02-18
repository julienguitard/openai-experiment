-- Normalized tables
DROP TABLE IF EXISTS chats CASCADE;

CREATE TABLE chats 
(
  chat_id   VARCHAR(128) PRIMARY KEY,
  created_at      TIMESTAMP,
  system_role      TEXT
);

DROP TABLE IF EXISTS qas CASCADE;

CREATE TABLE qas
(
  qa_id   VARCHAR(128) PRIMARY KEY,
  chat_id    VARCHAR(128) REFERENCES chats(chat_id),
  rank_      INT,
  prompt TEXT,
  response TEXT,
  retries INT DEFAULT 0);

