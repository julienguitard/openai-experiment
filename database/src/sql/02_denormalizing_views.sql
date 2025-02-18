-- Denormalizing (pure) views
DROP VIEW IF EXISTS chats_qas CASCADE;

CREATE VIEW chats_qas
AS
SELECT chat_id, 
       created_at,
       system_role, 
       qa_id,
       rank_,
       prompt,
       response,
       retries
FROM chats LEFT JOIN qas USING(chat_id);

