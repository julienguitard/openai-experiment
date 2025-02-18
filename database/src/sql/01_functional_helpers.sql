-- Functional (impure) helpers
DROP FUNCTION IF EXISTS generate_chat_id CASCADE;

CREATE OR REPLACE FUNCTION generate_chat_id(TIMESTAMP) RETURNS VARCHAR(128)
AS
$$
SELECT MD5(CAST($1 AS VARCHAR(128)))  $$ LANGUAGE SQL;

DROP FUNCTION IF EXISTS qa_id CASCADE;

CREATE OR REPLACE FUNCTION generate_qa_id(TIMESTAMP, INT)  RETURNS VARCHAR(128)
AS
$$
SELECT MD5(CAST($1 AS VARCHAR(128))||CAST($2 AS VARCHAR(128))) $$ LANGUAGE SQL;

DROP FUNCTION IF EXISTS generate_insertable_chat CASCADE;

CREATE OR REPLACE FUNCTION generate_insertable_chat(TIMESTAMP,TEXT) RETURNS chats
AS
$$
SELECT generate_chat_id($1) AS chat_id, $1 AS created_at, $2 AS system_role  $$ LANGUAGE SQL;

DROP FUNCTION IF EXISTS generate_insertable_qa CASCADE;

CREATE OR REPLACE FUNCTION generate_insertable_qa(TIMESTAMP,INT, TEXT,TEXT,INT) RETURNS qas
AS
$$
SELECT generate_chat_id($1) AS chat_id, generate_qa_id($1,$2) AS qa_id, $2 AS rank_, $3 AS prompt, $4 AS response, $5 AS retries  $$ LANGUAGE SQL;
