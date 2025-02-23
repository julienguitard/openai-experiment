-- Functional (impure) helpers
DROP FUNCTION IF EXISTS generate_chat_id CASCADE;

CREATE OR REPLACE FUNCTION generate_chat_id(BIGINT) RETURNS VARCHAR(128)
AS
$$
SELECT MD5(CAST($1 AS VARCHAR(128)))  $$ LANGUAGE SQL;

DROP FUNCTION IF EXISTS qa_id CASCADE;

CREATE OR REPLACE FUNCTION generate_qa_id(BIGINT, INT)  RETURNS VARCHAR(128)
AS
$$
SELECT MD5(CAST($1 AS VARCHAR(128))||CAST($2 AS VARCHAR(128))) $$ LANGUAGE SQL;

DROP FUNCTION IF EXISTS generate_insertable_chat CASCADE;

CREATE OR REPLACE FUNCTION generate_insertable_chat(BIGINT,TEXT) RETURNS chats
AS
$$
SELECT generate_chat_id($1) AS chat_id, TO_TIMESTAMP($1) AS created_at, $2::BYTEA AS system_role  $$ LANGUAGE SQL;

DROP FUNCTION IF EXISTS generate_insertable_qa CASCADE;

CREATE OR REPLACE FUNCTION generate_insertable_qa(BIGINT,INT, TEXT,TEXT,INT) RETURNS qas
AS
$$
SELECT generate_qa_id($1,$2) AS qa_id,generate_chat_id($1) AS chat_id, $2 AS rank_, $3::BYTEA AS prompt, $4::BYTEA AS response, $5 AS retries  $$ LANGUAGE SQL;
