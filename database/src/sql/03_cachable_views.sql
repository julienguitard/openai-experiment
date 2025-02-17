DROP VIEW IF EXISTS tmp_epochs_steps_latest_0 CASCADE;

CREATE VIEW tmp_epochs_steps_latest_0 
AS
SELECT t0.*
FROM tmp_epochs_steps t0
  JOIN (SELECT MAX(rank_) AS rank_ FROM tmp_epochs_steps) t1 USING (rank_);

DROP MATERIALIZED VIEW IF EXISTS tmp_positions_latest_0 CASCADE;

CREATE MATERIALIZED  VIEW tmp_positions_latest_0 
AS
SELECT *
FROM (SELECT t0.*
      FROM (SELECT *,
                   epoch_step_0['rank_']::INT AS rank_
            FROM tmp_positions) t0
        JOIN (SELECT MAX(epoch_step_0['rank_']::INT) AS rank_
              FROM tmp_positions) t1 USING (rank_));

DROP MATERIALIZED VIEW IF EXISTS tmp_positions_latest_on_0 CASCADE;

CREATE MATERIALIZED VIEW tmp_positions_latest_on_0
AS
SELECT *
FROM tmp_positions_latest_0
WHERE state = 1;

DROP MATERIALIZED VIEW IF EXISTS tmp_interactions_latest_0 CASCADE;

CREATE MATERIALIZED VIEW tmp_interactions_latest_0
AS
SELECT *
FROM (SELECT t0.*
      FROM (SELECT *,
                   position_0['epoch_step_0']['rank_']::INT AS rank_
            FROM tmp_interactions) t0
        JOIN (SELECT MAX(position_0['epoch_step_0']['rank_']::INT) AS rank_
              FROM tmp_interactions) t1 USING (rank_));

DROP MATERIALIZED VIEW IF EXISTS tmp_interactions_odds_latest_0 CASCADE;

CREATE MATERIALIZED VIEW tmp_interactions_odds_latest_0
AS
SELECT *
FROM (SELECT t0.*
      FROM (SELECT *,
                   interaction_0['position_0']['epoch_step_0']['rank_']::INT AS rank_
            FROM tmp_interactions_odds) t0
        JOIN (SELECT MAX(interaction_0['position_0']['epoch_step_0']['rank_']::INT) AS rank_
              FROM tmp_interactions_odds) t1 ON t0.rank_ = t1.rank_);
