DO $$
BEGIN
    IF (SELECT count(*) FROM migration_users) <> 1577 THEN RAISE EXCEPTION 'Falsche Personenanzahl'; END IF;
    IF (SELECT count(*) FROM migration_user_hobbies WHERE source = 'xml') <> 301 THEN RAISE EXCEPTION 'Falsche XML-Hobbyanzahl'; END IF;
    IF EXISTS (SELECT 1 FROM migration_user_hobbies WHERE source = 'xml' AND priority IS NOT NULL) THEN RAISE EXCEPTION 'XML-Priorität muss NULL sein'; END IF;
    IF EXISTS (SELECT email, hobby_name FROM migration_user_hobbies GROUP BY email, hobby_name HAVING count(*) > 1) THEN RAISE EXCEPTION 'Doppelte Person-Hobby-Zuordnung'; END IF;
    IF EXISTS (SELECT 1 FROM migration_rejections WHERE reason = '') THEN RAISE EXCEPTION 'Leere Ablehnungsbegründung'; END IF;
END $$;
SELECT 'Akt 3 eigene Prüfungen bestanden' AS status;
