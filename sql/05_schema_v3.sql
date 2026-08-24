ALTER TABLE migration_hobbies_data
    ALTER COLUMN priority DROP NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS migration_hobbies_person_hobby_unique
    ON migration_hobbies_data (person_id, hobby_name);

CREATE TABLE IF NOT EXISTS migration_rejections_data (
    source text NOT NULL,
    source_ref text NOT NULL,
    reason text NOT NULL CHECK (reason <> ''),
    PRIMARY KEY (source, source_ref)
);

CREATE TABLE IF NOT EXISTS migration_transfer_decisions (
    source text NOT NULL,
    source_ref text NOT NULL,
    outcome text NOT NULL,
    PRIMARY KEY (source, source_ref)
);

CREATE OR REPLACE VIEW migration_rejections (source, source_ref, reason) AS
SELECT source, source_ref, reason
FROM migration_rejections_data;
