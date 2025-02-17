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