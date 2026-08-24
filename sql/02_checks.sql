DO $$
BEGIN
    IF (SELECT count(*) FROM migration_users) <> 1576 THEN
        RAISE EXCEPTION 'Erwartet: 1576 Personen';
    END IF;

    IF EXISTS (SELECT 1 FROM migration_users WHERE email IS NULL OR email = '') THEN
        RAISE EXCEPTION 'Leere E-Mail-Adresse gefunden';
    END IF;

    IF EXISTS (
        SELECT lower(email)
        FROM migration_users
        GROUP BY lower(email)
        HAVING count(*) > 1
    ) THEN
        RAISE EXCEPTION 'E-Mail-Adressen sind nicht eindeutig';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM migration_users
        WHERE first_name IS NULL
           OR last_name IS NULL
           OR birth_date IS NULL
           OR postal_code IS NULL
           OR city IS NULL
    ) THEN
        RAISE EXCEPTION 'Pflichtfeld ist NULL';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM migration_users
        WHERE city = 'Demmin, Hansestadt'
    ) THEN
        RAISE EXCEPTION 'Komma im Ortsnamen wurde nicht erhalten';
    END IF;
END $$;

SELECT 'Akt 1 eigene Prüfungen bestanden' AS status;
