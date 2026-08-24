DO $$
BEGIN
    IF (SELECT count(*) FROM migration_users) <> 1576 THEN RAISE EXCEPTION 'Falsche Personenanzahl'; END IF;
    IF (SELECT count(*) FROM migration_user_interests) <> 1609 THEN RAISE EXCEPTION 'Falsche Interessenanzahl'; END IF;
    IF EXISTS (SELECT 1 FROM migration_users WHERE email = '' OR phone IS NULL OR gender IS NULL) THEN RAISE EXCEPTION 'Fehlende V2-Stammdaten'; END IF;
    IF EXISTS (SELECT 1 FROM migration_user_hobbies WHERE priority < -100 OR priority > 100 OR source <> 'excel') THEN RAISE EXCEPTION 'Ungültige Hobbydaten'; END IF;
    IF EXISTS (SELECT email, hobby_name, source FROM migration_user_hobbies GROUP BY email, hobby_name, source HAVING count(*) > 1) THEN RAISE EXCEPTION 'Doppelte Hobbyzuordnung'; END IF;
    IF EXISTS (SELECT liker_email FROM migration_likes WHERE liker_email = liked_email) THEN RAISE EXCEPTION 'Selbst-Like gefunden'; END IF;
    IF EXISTS (SELECT sender_email FROM migration_messages WHERE sender_email = receiver_email) THEN RAISE EXCEPTION 'Selbst-Nachricht gefunden'; END IF;
    IF EXISTS (SELECT 1 FROM migration_messages WHERE conversation_id IS NULL) THEN RAISE EXCEPTION 'Conversation-ID fehlt'; END IF;
END $$;
SELECT 'Akt 2 eigene Prüfungen bestanden' AS status;
