-- Normalized tables
DROP TABLE IF EXISTS tmp_epochs_steps_normalized CASCADE;

CREATE TABLE tmp_epochs_steps_normalized 
(
  epoch_step_id   VARCHAR(128) PRIMARY KEY,
  epoch           INT,
  step            INT,
  rank_           INT,
  max_step        INT DEFAULT 1,
  UNIQUE (epoch,step),
  CONSTRAINT valid_epoch_step CHECK (step IN (0,1,2))
);

DROP TABLE IF EXISTS tmp_boards_normalized CASCADE;

CREATE TABLE tmp_boards_normalized 
(
  board_id   VARCHAR(128) PRIMARY KEY,
  left_      INT DEFAULT 0,
  right_     INT DEFAULT 99,
  width      INT DEFAULT 100,
  CONSTRAINT valid_board CHECK ((right_ - left_) = (width - 1) AND (width > 0))
);

DROP TABLE IF EXISTS tmp_lines_normalized CASCADE;

CREATE TABLE tmp_lines_normalized 
(
  line_id                    VARCHAR(128) PRIMARY KEY,
  board_id                   VARCHAR(128) REFERENCES tmp_boards_normalized (board_id),
  x                          INT,
  bottom                     INT DEFAULT 0,
  top                        INT DEFAULT 99,
  initial_white_depth        INT DEFAULT 50,
  initial_interspace_depth   INT DEFAULT 1,
  initial_black_depth        INT DEFAULT 50,
  CONSTRAINT valid_line CHECK ((top - bottom) = ((initial_white_depth + initial_interspace_depth + initial_black_depth -2)) AND (initial_white_depth > 0) AND (initial_interspace_depth > 0) AND (initial_interspace_depth > 0))
);

DROP TABLE IF EXISTS tmp_squares_normalized CASCADE;

CREATE TABLE tmp_squares_normalized 
(
  square_id   VARCHAR(128) PRIMARY KEY,
  line_id     VARCHAR(128) REFERENCES tmp_lines_normalized (line_id),
  y           INT,
  UNIQUE (line_id,y)
);

DROP TABLE IF EXISTS tmp_roles_normalized CASCADE;

CREATE TABLE tmp_roles_normalized 
(
  role_id     VARCHAR(128) PRIMARY KEY,
  side        INT,
  role_name   VARCHAR(16)
);

DROP TABLE IF EXISTS tmp_actions_normalized CASCADE;

CREATE TABLE tmp_actions_normalized 
(
  action_id     VARCHAR(128) PRIMARY KEY,
  role_id_0     VARCHAR(128) REFERENCES tmp_roles_normalized (role_id),
  role_id_1     VARCHAR(128) REFERENCES tmp_roles_normalized (role_id),
  action_name   VARCHAR(16),
  UNIQUE (role_id_0,role_id_1)
);

DROP TABLE IF EXISTS tmp_odds_normalized CASCADE;

CREATE TABLE tmp_odds_normalized 
(
  odd_id      VARCHAR(128) PRIMARY KEY,
  action_id   VARCHAR(128) REFERENCES tmp_actions_normalized (action_id),
  is_on_0     INT,
  is_on_1     INT,
  proba       DOUBLE PRECISION,
  UNIQUE (action_id,is_on_0,is_on_1),
  CONSTRAINT valid_odds CHECK (((is_on_0) IN (0,1)) AND ((is_on_1) IN (0,1)) AND (proba >= 0) AND (proba <= 1))
);

DROP TABLE IF EXISTS tmp_pieces_normalized CASCADE;

CREATE TABLE tmp_pieces_normalized 
(
  piece_id            VARCHAR(128) PRIMARY KEY,
  initial_square_id   VARCHAR(128) REFERENCES tmp_squares_normalized (square_id),
  role_id             VARCHAR(128) REFERENCES tmp_roles_normalized (role_id),
  piece_name          VARCHAR(16)
);

DROP TABLE IF EXISTS tmp_positions_normalized CASCADE;

CREATE TABLE tmp_positions_normalized 
(
  position_id     VARCHAR(128) PRIMARY KEY,
  epoch_step_id   VARCHAR(128) REFERENCES tmp_epochs_steps_normalized (epoch_step_id),
  piece_id        VARCHAR(128) REFERENCES tmp_pieces_normalized (piece_id),
  square_id       VARCHAR(128) REFERENCES tmp_squares_normalized (square_id),
  state           INT,
  won             INT,
  UNIQUE (epoch_step_id,piece_id),
  CONSTRAINT valid_position CHECK (state IN (0,1) AND won IN (1,0) )
);

DROP TABLE IF EXISTS tmp_interactions_normalized CASCADE;

CREATE TABLE tmp_interactions_normalized 
(
  interaction_id   VARCHAR(128) PRIMARY KEY,
  position_id_0    VARCHAR(128) REFERENCES tmp_positions_normalized (position_id),
  position_id_1    VARCHAR(128) REFERENCES tmp_positions_normalized (position_id),
  action_id        VARCHAR(128) REFERENCES tmp_actions_normalized (action_id),
  UNIQUE (position_id_0,position_id_1,action_id)
);

DROP TABLE IF EXISTS tmp_interactions_odds_normalized CASCADE;

CREATE TABLE tmp_interactions_odds_normalized 
(
  interaction_odd_id   VARCHAR(128) PRIMARY KEY,
  interaction_id       VARCHAR(128) REFERENCES tmp_interactions_normalized (interaction_id),
  odd_id               VARCHAR(128) REFERENCES tmp_odds_normalized (odd_id),
  UNIQUE (interaction_id,odd_id)
);