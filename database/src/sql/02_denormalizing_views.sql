-- Denormalizing (pure) views
DROP VIEW IF EXISTS tmp_epochs_steps CASCADE;

CREATE VIEW tmp_epochs_steps 
AS
SELECT t0.epoch_step_id,
       t0.epoch,
       t0.step,
       t0.rank_,
       t0.max_step,
       t1.epoch_step_id AS previous_epoch_step_id,
       t2.epoch_step_id AS next_epoch_step_id
FROM (SELECT *,
             CASE
               WHEN step > 0 THEN epoch
               ELSE epoch - 1
             END AS previous_epoch,
             CASE
               WHEN step > 0 THEN step - 1
               ELSE max_step
             END AS previous_step,
             CASE
               WHEN step < max_step THEN epoch
               ELSE epoch +1
             END AS next_epoch,
             CASE
               WHEN step < max_step THEN step + 1
               ELSE 0
             END AS next_step
      FROM tmp_epochs_steps_normalized) t0
  LEFT JOIN tmp_epochs_steps_normalized t1
         ON t0.previous_epoch = t1.epoch
        AND t0.previous_step = t1.step
  LEFT JOIN tmp_epochs_steps_normalized t2
         ON t0.next_epoch = t2.epoch
        AND t0.next_step = t2.step;

DROP VIEW IF EXISTS tmp_boards CASCADE;

CREATE VIEW tmp_boards 
AS
SELECT *
FROM tmp_boards_normalized;

DROP VIEW IF EXISTS tmp_lines CASCADE;

CREATE VIEW tmp_lines 
AS
SELECT t0.*,
       TO_JSONB(t1.*) AS board_0
FROM tmp_lines_normalized t0
  JOIN tmp_boards t1 USING (board_id);

DROP VIEW IF EXISTS tmp_squares CASCADE;

CREATE VIEW tmp_squares 
AS
SELECT t0.*,
       TO_JSONB(t1.*) AS line_0
FROM tmp_squares_normalized t0
  JOIN tmp_lines t1 USING (line_id);

DROP VIEW IF EXISTS tmp_roles CASCADE;

CREATE VIEW tmp_roles 
AS
SELECT *
FROM tmp_roles_normalized;

DROP VIEW IF EXISTS tmp_actions CASCADE;

CREATE VIEW tmp_actions 
AS
SELECT t0.*,
       TO_JSONB(t1.*) AS role_0,
       TO_JSONB(t2.*) AS role_1
FROM tmp_actions_normalized t0
  JOIN tmp_roles t1 ON t0.role_id_0 = t1.role_id
  JOIN tmp_roles t2 ON t0.role_id_1 = t2.role_id;

DROP VIEW IF EXISTS tmp_odds CASCADE;

CREATE VIEW tmp_odds 
AS
SELECT t0.*,
       TO_JSONB(t1.*) AS action_0
FROM tmp_odds_normalized t0
  JOIN tmp_actions t1 USING (action_id);

DROP VIEW IF EXISTS tmp_odds_with_cumulative CASCADE;

CREATE VIEW tmp_odds_with_cumulative 
AS
SELECT *,
       SUM(proba) OVER (PARTITION BY action_id,action_0['role_id_0'],action_0['role_id_0'] ORDER BY is_on_0,is_on_1) AS upper_cumulative_proba,
       1 -(SUM(proba) OVER (PARTITION BY action_id,action_0['role_id_0'],action_0['role_id_0'] ORDER BY is_on_0 DESC,is_on_1 DESC)) AS lower_cumulative_proba
FROM (SELECT t0.*,
             t1.proba AS proba_0_0
      FROM tmp_odds t0
        JOIN (SELECT action_id,
                     proba
              FROM tmp_odds
              WHERE is_on_0 = 0
              AND   is_on_1 = 0) t1 USING (action_id));

DROP VIEW IF EXISTS tmp_pieces CASCADE;

CREATE VIEW tmp_pieces 
AS
SELECT t0.*,
       TO_JSONB(t1.*) AS role_0,
       TO_JSONB(t2.*) AS square_0
FROM tmp_pieces_normalized t0
  JOIN tmp_roles t1 USING (role_id)
  JOIN tmp_squares t2 ON t0.initial_square_id = t2.square_id;

DROP VIEW IF EXISTS tmp_positions CASCADE;

CREATE VIEW tmp_positions 
AS
SELECT t0.*,
       TO_JSONB(t1.*) AS epoch_step_0,
       TO_JSONB(t2.*) AS piece_0,
       TO_JSONB(t3.*) AS square_0
FROM tmp_positions_normalized t0
  JOIN tmp_epochs_steps t1 USING (epoch_step_id)
  JOIN tmp_pieces t2 USING (piece_id)
  JOIN tmp_squares t3 USING (square_id);

DROP VIEW IF EXISTS tmp_interactions CASCADE;

CREATE VIEW tmp_interactions 
AS
SELECT t0.*,
       TO_JSONB(t1.*) AS position_0,
       TO_JSONB(t2.*) AS position_1,
       TO_JSONB(t3.*) AS action_0
FROM tmp_interactions_normalized t0
  JOIN tmp_positions t1 ON t0.position_id_0 = t1.position_id
  JOIN tmp_positions t2 ON t0.position_id_1 = t2.position_id
  JOIN tmp_actions t3 USING (action_id);

DROP VIEW IF EXISTS tmp_interactions_odds CASCADE;

CREATE VIEW tmp_interactions_odds 
AS
SELECT t0.*,
       TO_JSONB(t1.*) AS interaction_0,
       TO_JSONB(t2.*) AS odd_0
FROM tmp_interactions_odds_normalized t0
  JOIN tmp_interactions t1 USING (interaction_id)
  JOIN tmp_odds_with_cumulative t2 USING (odd_id);

--Additional constraint (pure) views
DROP VIEW IF EXISTS tmp_boards_errors_messages CASCADE;

CREATE VIEW tmp_boards_errors_messages 
AS
SELECT 'epoch_step' AS entity,
       'epochs not contiguous' AS message
FROM (SELECT MAX(epoch) -MIN(epoch) + 1 - COUNT(epoch) AS contig_
      FROM (SELECT DISTINCT epoch FROM tmp_epochs_steps))
WHERE contig_ != 0
UNION ALL
SELECT 'board' AS entity,
       'x not contiguous for board_id ' || board_id AS message
FROM (SELECT board_id,
             MAX(x) -MIN(x) + 1 - COUNT(x) AS contig_
      FROM tmp_lines
      GROUP BY board_id)
WHERE contig_ != 0
UNION ALL
SELECT 'line' AS entity,
       'lines not connected board_id ' || board_id || ' and x_0=' ||line_0['x'] AS message
FROM (SELECT board_id,
             line_0
      FROM (SELECT t0.board_id,
                   TO_JSONB(t0.*) AS line_0,
                   TO_JSONB(t1.*) AS line_1
            FROM tmp_lines t0
              JOIN tmp_lines t1
                ON t0.board_id = t1.board_id
               AND (t0.x +1) = t1.x)
      WHERE (line_0['bottom'] > line_1['top'])
      OR    (line_1['bottom'] > line_0['top']))
UNION ALL
SELECT 'square' AS entity,
       'x not contiguous for board_id ' || board_id || ' and x=' ||x AS message
FROM (SELECT board_id,
             x,
             MAX(y) -MIN(y) + 1 - COUNT(y) AS contig_
      FROM (SELECT line_0['board_id']::VARCHAR(128) AS board_id,
                   line_0['x']::VARCHAR(128) AS x,
                   y
            FROM tmp_squares)
      GROUP BY board_id,
               x)
WHERE contig_ != 0
UNION ALL
SELECT 'odd' AS entity,
       CASE
         WHEN cnt != 4 THEN 'odds are not 4 per action_id' || action_id
         ELSE 'sum of proba is not close to 1.0 for action_id ' ||action_id
       END AS message
FROM (SELECT action_id,
             COUNT(odd_id) AS cnt,
             SUM(proba) AS sum_proba
      FROM tmp_odds
      GROUP BY action_id)
WHERE (cnt != 4)
OR    ABS(1 - sum_proba) > 1e-6
UNION ALL
SELECT 'square' AS entity,
       'initial_square_id inconsistent for position_id ' ||position_id AS message
FROM (SELECT t0.position_id,
             t0.piece_id,
             t0.square_id,
             t1.initial_square_id
      FROM (SELECT *
            FROM tmp_positions
            WHERE epoch_step_0['epoch']::INT = 0
            AND   epoch_step_0['step']::INT = 0) t0
        JOIN tmp_pieces t1 USING (piece_id))
WHERE square_id != initial_square_id
UNION ALL
SELECT 'interactions' AS entity,
       CASE
         WHEN (position_0['epoch_step_id'] != position_1['epoch_step_id']) THEN 'epochs_steps not the same for ' ||interaction_id
         WHEN (position_0['piece_0,role_id'] != action_0['role_id_0']) THEN 'first role note the same for ' ||interaction_id
         ELSE 'second role note the same for ' ||interaction_id
       END AS message
FROM (SELECT *
      FROM tmp_interactions
      WHERE (position_0['epoch_step_id'] != position_1['epoch_step_id'])
      OR    (position_0['piece_0,role_id'] != action_0['role_id_0'])
      OR    (position_1['piece_0,role_id'] != action_0['role_id_1']))
UNION ALL
SELECT 'interactions_odds' AS entity,
       'action_id different for ' ||interaction_odd_id AS message
FROM (SELECT t0.interaction_odd_id,
             t0.interaction_0['action_0,action_id'] AS action_id_0,
             t0.odd_0['action_0,action_id'] AS action_id_1
      FROM tmp_interactions_odds t0
        JOIN tmp_odds t1 USING (odd_id))
WHERE action_id_0 != action_id_1;