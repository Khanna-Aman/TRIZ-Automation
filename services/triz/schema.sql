-- TRIZ data schema (Postgres)
-- Tables: principles (1..40), parameters (1..39), matrix_link (parameter pair -> principle)

CREATE TABLE IF NOT EXISTS triz_principle (
  id SMALLINT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT
);

CREATE TABLE IF NOT EXISTS triz_parameter (
  id SMALLINT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT
);

-- Normalized mapping table: one row per (improving, worsening, principle)
CREATE TABLE IF NOT EXISTS triz_matrix_link (
  improving_param SMALLINT NOT NULL REFERENCES triz_parameter(id) ON DELETE CASCADE,
  worsening_param SMALLINT NOT NULL REFERENCES triz_parameter(id) ON DELETE CASCADE,
  principle_id SMALLINT NOT NULL REFERENCES triz_principle(id) ON DELETE CASCADE,
  PRIMARY KEY (improving_param, worsening_param, principle_id)
);

CREATE INDEX IF NOT EXISTS idx_triz_matrix_pair ON triz_matrix_link (improving_param, worsening_param);

